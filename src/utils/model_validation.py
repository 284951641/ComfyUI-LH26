"""Local-only validation for separately uploaded LH2.6 model files.

This module never downloads, modifies, renames, or deletes model files.
"""

import hashlib
import json
import os
from typing import Optional

from .constants import (
    DOWNLOAD_CHUNK_SIZE,
    find_model_file,
    get_all_model_paths,
    get_base_cache_dir,
    get_validation_cache_path,
)
from .model_registry import MODEL_REGISTRY


def _load_cache(cache_dir: str) -> dict:
    path = get_validation_cache_path(cache_dir)
    try:
        with open(path, "r", encoding="utf-8") as handle:
            return json.load(handle)
    except (FileNotFoundError, OSError, ValueError, TypeError):
        return {}


def _save_cache(cache: dict, cache_dir: str) -> None:
    path = get_validation_cache_path(cache_dir)
    try:
        os.makedirs(os.path.dirname(path), exist_ok=True)
        with open(path, "w", encoding="utf-8") as handle:
            json.dump(cache, handle, indent=2)
    except OSError:
        # Read-only hosted environments can still run; they only revalidate.
        pass


def _valid_safetensors_header(path: str) -> bool:
    try:
        size = os.path.getsize(path)
        with open(path, "rb") as handle:
            header_size = int.from_bytes(handle.read(8), "little")
        return 0 < header_size < size
    except OSError:
        return False


def _validate_file(path: str, expected_hash: Optional[str], cache_dir: str) -> bool:
    if not os.path.isfile(path) or os.path.getsize(path) == 0:
        return False
    if path.endswith(".safetensors") and not _valid_safetensors_header(path):
        return False

    cache = _load_cache(cache_dir)
    name = os.path.basename(path)
    stat = os.stat(path)
    cached = cache.get(name, {})
    if (
        expected_hash
        and cached.get("sha256") == expected_hash
        and cached.get("size") == stat.st_size
        and abs(cached.get("mtime", 0) - stat.st_mtime) < 2
    ):
        return True

    if expected_hash:
        digest = hashlib.sha256()
        with open(path, "rb") as handle:
            for chunk in iter(lambda: handle.read(DOWNLOAD_CHUNK_SIZE), b""):
                digest.update(chunk)
        if digest.hexdigest().lower() != expected_hash.lower():
            return False
        cache[name] = {
            "sha256": expected_hash.lower(),
            "size": stat.st_size,
            "mtime": stat.st_mtime,
        }
        _save_cache(cache, cache_dir)
    return True


def validate_required_models(
    dit_model: str,
    vae_model: str,
    model_dir: Optional[str] = None,
    debug=None,
) -> bool:
    """Validate both selected files without changing them."""

    cache_dir = model_dir or get_base_cache_dir()
    ok = True
    for filename in (dit_model, vae_model):
        info = MODEL_REGISTRY.get(filename)
        model_type = "VAE" if info and info.category == "vae" else "DiT"
        path = find_model_file(filename, fallback_dir=cache_dir)
        if not info or not os.path.isfile(path):
            ok = False
            if debug:
                debug.log(
                    f"Missing {model_type} model: {filename}. Searched: "
                    + ", ".join(get_all_model_paths()),
                    level="ERROR",
                    category="setup",
                    force=True,
                )
            continue
        if not _validate_file(path, info.sha256, cache_dir):
            ok = False
            if debug:
                debug.log(
                    f"Invalid {model_type} model (file was not changed): {path}",
                    level="ERROR",
                    category="setup",
                    force=True,
                )
        elif debug:
            debug.log(f"Validated {model_type} model: {path}", category="setup")
    return ok
