---
description: 对智慧养蜂 Windows 交付包执行分层门禁审计
argument-hint: "[交付目录或候选版本]"
---
# Windows 交付门禁

只读检查 ${@:-当前交付候选}。先运行可用的本地结构测试，再核对 Windows x86_64 NVIDIA 黑盒合同：自包含 onedir、仅 ONNX、CUDA provider 不静默回退、stdout 恰好一行 JSON、成功/404/501 错误码、路径边界、重复运行确定性、≤10 秒、≤16GB VRAM、依赖与 SHA-256 清单。缺少 Windows/GPU 环境时明确标记 NOT RUN，不得用 Mac 检查冒充最终验收。除非授权，不打包、不上传、不提交比赛。
