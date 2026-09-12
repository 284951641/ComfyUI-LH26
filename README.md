# ComfyUI-LH26

LH2.6 视频增强节点，适配标准 ComfyUI（Linux/Windows）及 RunningHub 节点审核流程。

## 节点

- `LH2.6 (Down)Load DiT Model`
- `LH2.6 (Down)Load VAE Model`
- `LH2.6 Video Upscaler`
- `LH2.6 Torch Compile Settings`（可选）

## 安装

将本仓库放入：

```text
ComfyUI/custom_nodes/ComfyUI-LH26
```

安装依赖：

```bash
cd ComfyUI/custom_nodes/ComfyUI-LH26
python -m pip install -r requirements.txt
```

## 模型文件

模型不放入 GitHub 节点仓库。请通过平台模型上传/审核功能分别上传以下文件，并保持文件名不变：

```text
lh26_dit_3b_bf16.safetensors
lh26_vae_bf16.safetensors
```

节点会同时搜索 RunningHub 常用的 `unet` 目录和标准 ComfyUI 目录：

```text
ComfyUI/models/LH2.6/lh26_dit_3b_bf16.safetensors
ComfyUI/models/LH2.6/lh26_vae_bf16.safetensors
ComfyUI/models/unet/lh26_dit_3b_bf16.safetensors
ComfyUI/models/unet/lh26_vae_bf16.safetensors
```

如果 RunningHub 上传页只有 `UNet` 类型，两个文件都选择 `UNet` 即可；节点会自动在该目录找到它们。

`pos_emb.pt` 和 `neg_emb.pt` 体积很小，已随节点包提供。

## RunningHub

1. 向 RunningHub 提交本 GitHub 仓库链接审核节点。
2. 单独提交两个模型文件审核/上传（上传页只有 `UNet` 时两个都选 `UNet`）。
3. 审核收录后，导入 `example_workflows/LH2.6-RunningHub-video.json`。
4. 上传输入视频并运行。

## 推荐初始参数

- DiT：`cuda:0`，`blocks_to_swap=32`，`offload_device=cpu`，`attention_mode=sdpa`
- VAE：`cuda:0`，开启 tiled encode/decode，`offload_device=cpu`
- 输出短边：1080
- batch size：显存不足时使用 5 或 9

## License

Apache-2.0，详见 `LICENSE`。
