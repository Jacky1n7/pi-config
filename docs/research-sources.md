# 设计依据

- Pi 官方 context files、project trust、security、skills、prompts、extensions、themes、packages、settings 文档：本机安装的 `@earendil-works/pi-coding-agent/docs/`。
- AGENTS.md：<https://agents.md/>；OpenAI Codex 指南：<https://developers.openai.com/codex/guides/agents-md>。
- PyTorch 可复现性：<https://docs.pytorch.org/docs/stable/notes/randomness.html>。
- pytest markers：<https://docs.pytest.org/en/stable/how-to/mark.html>；Ruff 配置：<https://docs.astral.sh/ruff/configuration/>。
- DVC 数据/模型版本：<https://dvc.org/doc/use-cases/versioning-data-and-models>；MLflow Tracking：<https://mlflow.org/docs/latest/ml/tracking/>。
- MCP 安全最佳实践：<https://modelcontextprotocol.io/specification/2025-06-18/basic/security_best_practices>。
- GitHub 大文件：<https://docs.github.com/en/repositories/working-with-files/managing-large-files/about-large-files-on-github>。

采用原则：全局规则短且稳定；项目规则具体且可执行；数据、切分、配置、指标和产物可追溯；Extension/MCP 视为有系统权限的供应链依赖；安装必须可 dry-run、备份、回滚和复现。
