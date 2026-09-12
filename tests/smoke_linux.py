"""Linux smoke test against an actual ComfyUI checkout."""

from __future__ import annotations

import asyncio
import importlib.util
import json
import sys
import traceback
from pathlib import Path

def main() -> None:
    repo = Path(__file__).resolve().parents[1]
    comfy = Path(sys.argv[1]).resolve()
    sys.path.insert(0, str(comfy))

    spec = importlib.util.spec_from_file_location(
        "comfyui_lh26", repo / "__init__.py", submodule_search_locations=[str(repo)]
    )
    if spec is None or spec.loader is None:
        raise RuntimeError("Cannot create LH2.6 package spec")
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)

    extension = asyncio.run(module.comfy_entrypoint())
    nodes = asyncio.run(extension.get_node_list())
    class_names = {node.__name__ for node in nodes}
    expected_classes = {"LH26LoadDiTModel", "LH26LoadVAEModel", "LH26VideoUpscaler", "LH26TorchCompileSettings"}
    if class_names != expected_classes:
        raise AssertionError(f"node classes: {class_names!r}")

# Build every V3 schema. This catches API drift and missing imports.
    for node in nodes:
        schema = node.define_schema()
        if schema is None:
            raise AssertionError(f"No schema for {node.__name__}")

    workflow = json.loads((repo / "example_workflows" / "LH2.6-RunningHub-video.json").read_text(encoding="utf-8"))
    workflow_types = {item.get("type") for item in workflow["nodes"]}
    required_workflow = {"LH26LoadDiTModel", "LH26LoadVAEModel", "LH26VideoUpscaler"}
    if not required_workflow <= workflow_types:
        raise AssertionError(f"workflow nodes: {required_workflow - workflow_types!r}")

    print("LH2.6 Linux/ComfyUI smoke import: OK")
    print("Nodes:", ", ".join(sorted(workflow_types & class_names)))


try:
    main()
except Exception as exc:
    detail = " ".join(traceback.format_exception_only(type(exc), exc)).strip()
    print(f"::error file=tests/smoke_linux.py,line=1::{detail}")
    raise
