"""Linux smoke test against an actual ComfyUI checkout."""

from __future__ import annotations

import asyncio
import importlib.util
import json
import sys
from pathlib import Path

repo = Path(__file__).resolve().parents[1]
comfy = Path(sys.argv[1]).resolve()
sys.path.insert(0, str(comfy))

spec = importlib.util.spec_from_file_location(
    "comfyui_lh26",
    repo / "__init__.py",
    submodule_search_locations=[str(repo)],
)
if spec is None or spec.loader is None:
    raise RuntimeError("Cannot create LH2.6 package spec")
module = importlib.util.module_from_spec(spec)
sys.modules[spec.name] = module
spec.loader.exec_module(module)

extension = asyncio.run(module.comfy_entrypoint())
nodes = asyncio.run(extension.get_node_list())
class_names = {node.__name__ for node in nodes}
expected_classes = {
    "LH26LoadDiTModel",
    "LH26LoadVAEModel",
    "LH26VideoUpscaler",
    "LH26TorchCompileSettings",
}
if class_names != expected_classes:
    raise AssertionError((class_names, expected_classes))

# Build every V3 schema. This catches API drift and missing imports.
for node in nodes:
    schema = node.define_schema()
    if schema is None:
        raise AssertionError(f"No schema for {node.__name__}")

workflow = json.loads(
    (repo / "example_workflows" / "LH2.6-RunningHub-video.json").read_text(encoding="utf-8")
)
workflow_types = {item.get("type") for item in workflow["nodes"]}
required_workflow = {
    "LH26LoadDiTModel",
    "LH26LoadVAEModel",
    "LH26VideoUpscaler",
}
if not required_workflow <= workflow_types:
    raise AssertionError(required_workflow - workflow_types)

print("LH2.6 Linux/ComfyUI smoke import: OK")
print("Nodes:", ", ".join(sorted(workflow_types & class_names)))
