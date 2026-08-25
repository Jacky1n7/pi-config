<!-- markdownlint-disable MD041 -->

## Pi 工作流补充

- 复杂研究改动先用 `/experiment-plan` 固化假设、plant-disjoint split、主指标、冻结点和算力预算；普通代码修复直接执行并按 `/validate-change` 验证。
- 多代理默认只并行侦察、外部研究和审查；当前工作树只允许一个写入者。已有实验/评估改动未提交时禁止 worktree 清理、reset、checkout、stash 或批量暂存。
- 代码审查优先检查：植物级独立性、测试/holdout 泄漏、人工尺寸参与预测选择、直接身份指标缺失、配置/种子/哈希缺失、deterministic bootstrap 被误写成优化 3DGS、sequence-aware 被误写成 4D。
- 验证阶梯：Markdown/配置解析 → 定向 pytest → `make lint` → 共享契约的 `make test` → 安全数据集 `make dry-run`。完整 pipeline、远端 GPU、sealed test 和大型产物生成必须明确授权。
- 项目级 Skill：`plant-scientific-workflow`；Prompt：`/experiment-plan`、`/validate-change`、`/manuscript-evidence`。
