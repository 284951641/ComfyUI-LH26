"""LH2.6 video enhancement nodes for ComfyUI."""

from .src.optimization.compatibility import ensure_triton_compat  # noqa: F401
from .src.interfaces import comfy_entrypoint, LH26Extension

__all__ = ["comfy_entrypoint", "LH26Extension"]
