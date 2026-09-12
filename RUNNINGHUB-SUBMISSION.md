# RunningHub 提交清单

## 1. 节点（只提交一个 GitHub 链接）

提交整个 `ComfyUI-LH26` 仓库，不拆分节点。审核后它会一次提供三个必需节点和一个可选设置节点。

## 2. 模型（与 GitHub 仓库分开上传）

| 文件 | SHA256 | 安装目录 |
|---|---|---|
| `lh26_dit_3b_bf16.safetensors` | `0e47fc2e3e953917fd9448101953c02dae21792d58143f3aa4d91a8b17cec8f9` | `UNet`（或 `ComfyUI/models/LH2.6/`） |
| `lh26_vae_bf16.safetensors` | `044d35c8332b5e8e89abde2729ff9015e5a11701ccd39c6f7f997b19d5be64a3` | `UNet`（或 `ComfyUI/models/LH2.6/`） |

请保持文件名不变。模型不应提交到 GitHub。若上传页面没有 VAE 类型，两个文件都选择 `UNet`；节点兼容 RunningHub 的该目录。

## 3. 工作流

模型和节点都收录后，上传 `example_workflows/LH2.6-RunningHub-video.json`。
