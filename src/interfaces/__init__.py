"""
LH2.6 ComfyUI Nodes
Central registry for all LH2.6 nodes
"""

from comfy_api.latest import ComfyExtension, io

from .video_upscaler import LH26VideoUpscaler
from .dit_model_loader import LH26LoadDiTModel
from .vae_model_loader import LH26LoadVAEModel
from .torch_compile_settings import LH26TorchCompileSettings


class LH26Extension(ComfyExtension):
    """LH2.6 ComfyUI Extension"""
    
    async def get_node_list(self) -> list[type[io.ComfyNode]]:
        """Return list of all LH2.6 nodes"""
        return [
            LH26VideoUpscaler,
            LH26LoadDiTModel,
            LH26LoadVAEModel,
            LH26TorchCompileSettings,
        ]


async def comfy_entrypoint() -> ComfyExtension:
    """ComfyUI V3 entry point"""
    return LH26Extension()


__all__ = [
    'LH26VideoUpscaler',
    'LH26LoadDiTModel',
    'LH26LoadVAEModel',
    'LH26TorchCompileSettings',
    'LH26Extension',
    'comfy_entrypoint',
]