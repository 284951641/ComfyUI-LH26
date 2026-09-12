"""LH2.6 model registry.

Large weights are distributed separately from the custom-node repository.
RunningHub installs this node package and places reviewed model files in
``ComfyUI/models/LH2.6``.
"""

from dataclasses import dataclass
from typing import List, Optional

from ..models.dit_3b.nadit import NaDiT as NaDiT3B
from ..models.video_vae_v3.modules.attn_video_vae import VideoAutoencoderKLWrapper

MODEL_CLASSES = {
    "dit_3b.nadit": NaDiT3B,
    "video_vae_v3.modules.attn_video_vae": VideoAutoencoderKLWrapper,
}

@dataclass
class ModelInfo:
    category: str = "dit"
    precision: str = "bf16"
    size: str = "3B"
    variant: Optional[str] = None
    sha256: Optional[str] = None

MODEL_REGISTRY = {
    "lh26_dit_3b_bf16.safetensors": ModelInfo(
        category="dit", precision="bf16", size="3B",
        sha256="0e47fc2e3e953917fd9448101953c02dae21792d58143f3aa4d91a8b17cec8f9",
    ),
    "lh26_vae_bf16.safetensors": ModelInfo(
        category="vae", precision="bf16", size="3B",
        sha256="044d35c8332b5e8e89abde2729ff9015e5a11701ccd39c6f7f997b19d5be64a3",
    ),
}

DEFAULT_DIT = "lh26_dit_3b_bf16.safetensors"
DEFAULT_VAE = "lh26_vae_bf16.safetensors"

def get_default_models(category: str) -> List[str]:
    return [name for name, info in MODEL_REGISTRY.items() if info.category == category]

def get_available_dit_models() -> List[str]:
    return get_default_models("dit")

def get_available_vae_models() -> List[str]:
    return get_default_models("vae")
