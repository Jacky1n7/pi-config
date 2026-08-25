# Jacky's Pi Workflow

[![Pi](https://img.shields.io/badge/Pi-0.84.3-8A2BE2)](https://pi.dev)
[![Packages](https://img.shields.io/badge/packages-17-blue)](manifest/packages.json)
[![MCP](https://img.shields.io/badge/MCP-2-orange)](config/mcp/servers.json)
[![License: MIT](https://img.shields.io/badge/license-MIT-success)](LICENSE)

这是我的个人 Pi 配置与科学 ML/CV 工作流仓库。它不再是“安装一堆最新版插件”的脚本，而是一套**锁版本、可审计、可 dry-run、可备份回滚、可按项目覆盖**的配置即代码方案。

重点适配：

- [`plant-geometry-phenotyping-lab`](templates/plant-geometry-phenotyping-lab)：植物多视角三维重建、GeoProMatch、3DGS artifact contract、器官身份与表型评估、论文证据链。
- [`smart-beekeeping-challenge-cup`](templates/smart-beekeeping-challenge-cup)：蜜蜂 YOLO 检测、BeeTracker、行为量化、CVAT、AutoDL GPU 训练和 Windows 黑盒交付。

## 核心原则

1. 全局 `AGENTS.md` 只放稳定的跨项目规则；项目事实、命令和科研约束放项目 `AGENTS.md`。
2. Extension、Skill、MCP 都按可执行供应链依赖管理；17 个 Pi 包和 2 个 MCP server 使用精确版本。
3. 禁止无人值守 `pi update --all`。升级必须更新 lock manifest、审查、验证、提交后再 apply。
4. 安装器只管理明确文件/键，不读取或复制 `auth.json`、provider credential、session、memory、cache、日志或真实 MCP token/env/header。
5. 每次 apply 先备份到 `${XDG_STATE_HOME:-~/.local/state}/pi-config/backups/`，支持按 transaction 回滚。
6. 科学/ML结果必须绑定代码、脏工作树、数据/切分、配置、种子、环境/硬件、指标口径和产物哈希。

## 快速开始

```bash
git clone https://github.com/Jacky1n7/pi-config.git
cd pi-config

# 1. 只打印计划，不修改系统
./install.sh

# 2. 应用 Jacky 的模型/UI profile；已安装且版本正确时可跳过包安装
./install.sh --apply --profile jacky

# 当前机器已经是锁定版本时
./install.sh --apply --profile jacky --skip-packages

# 3. 验证仓库与实际安装
./scripts/check.sh
./scripts/check.sh --installed --profile jacky
```

修改 context files、Prompts 或 Skills 后，重启 Pi 或运行 `/reload`。

### 应用重点项目模板

```bash
# 先 dry-run
./scripts/apply-project.sh plant-geometry-phenotyping-lab \
  ~/plant-geometry-phenotyping-lab
./scripts/apply-project.sh smart-beekeeping-challenge-cup \
  ~/挑战杯智慧养蜂项目

# 审查计划后应用
./scripts/apply-project.sh plant-geometry-phenotyping-lab \
  ~/plant-geometry-phenotyping-lab --apply
./scripts/apply-project.sh smart-beekeeping-challenge-cup \
  ~/挑战杯智慧养蜂项目 --apply
```

项目模板会：

- 合并项目 `.pi/` Prompts/Skills/Settings；
- 安装 `.pi-lens.json`；
- 在根 `AGENTS.md` 中维护一个带 marker 的 Pi workflow 区块；
- 修改前创建独立 transaction backup；
- 不碰项目代码、原始数据、模型、训练产物和用户其他未提交改动。

新增 `.pi` 资源后，Pi 首次进入仓库会要求 project trust；这是预期的安全边界。

## 配置结构

```text
manifest/packages.json              # 17 个 Pi package 精确版本，唯一来源
config/pi/settings.defaults.json    # 通用非密钥默认项
config/pi/settings.jacky.json       # Jacky 的模型/UI profile
config/mcp/servers.json             # 精确版本 MCP 命令
config/pi-lens/config.json          # 全局 Pi Lens 基线
global/AGENTS.md                    # 全局上下文规则
global/prompts/                     # /debug /test-fix /release-check /handoff
global/skills/scientific-ml-experiment/
templates/plant-geometry-phenotyping-lab/
templates/smart-beekeeping-challenge-cup/
scripts/pi_config.py                # apply/check/rollback 实现
scripts/check.sh
scripts/apply-project.sh
scripts/rollback.sh
```

兼容入口 `install.sh`、`update.sh`、`mcp.json`、`settings.defaults.json` 仍保留。`config.json` 只是人类可读索引，不再复制 package 清单。

## 17 个锁定 Pi 包

| 领域 | 包 |
| --- | --- |
| 编排 | `pi-subagents@0.56.0`、`@narumitw/pi-plan-mode@0.55.0`、`@narumitw/pi-goal@0.54.0`、`@juicesharp/rpiv-todo@2.7.1` |
| 代码质量 | `pi-lens@4.1.2`、`pi-simplify@0.2.3` |
| 上下文与记忆 | `context-mode@1.0.169`、`pi-hermes-memory@0.9.6` |
| Web/MCP/浏览器 | `pi-web-access@0.24.2`、`pi-mcp-adapter@2.27.0`、`pi-playwright@0.1.1` |
| Git/PR/UI | `@narumitw/pi-github-pr@0.49.6`、`@firstpick/pi-prompts-git-pr@0.1.6`、`@narumitw/pi-statusline@0.49.13` |
| 研究/生态/主题 | `@firstpick/pi-skill-deep-research@0.1.9`、`pi-marketplace@0.1.3`、`@victor-software-house/pi-curated-themes@0.2.1` |

机器可读详情见 [`manifest/packages.json`](manifest/packages.json)。

## 工具选择约定

- 本地事实：代码、测试、配置、Git、项目文档。
- 最新库/API文档：Context7。
- 一般网页研究和内容抓取：Web Access。
- 重复浏览器交互：Playwright。
- Console、Network、性能与 Lighthouse：Chrome DevTools MCP。
- 大日志、测试输出、JSON、仓库统计：Context Mode。
- 多步骤：Todo；只读方案：Plan；自主闭环：Goal；并行侦察/审查：Subagents；重大决策交叉质询：Council。

详细规则由 [`global/AGENTS.md`](global/AGENTS.md) 安装到 `~/.pi/agent/AGENTS.md`。

## 项目工作流

### Plant Geometry Phenotyping

提供：

- `/experiment-plan`：植物级独立、冻结切分、直接身份指标、预注册门禁；
- `/validate-change`：pytest/lint/full test/dry-run 分层验证；
- `/manuscript-evidence`：论文 claim 与 per-plant artifact 证据核对；
- `plant-scientific-workflow` Skill；
- 忽略 data/outputs/artifacts/manuscript build products 的 Pi Lens 配置。

关键边界：不使用人工尺寸在测试阶段选择预测器官；不把 deterministic bootstrap 描述成优化 3DGS；没有显式时变非刚性建模时不声称“4D”。

### Smart Beekeeping Challenge Cup

提供：

- `/competition-review`：赛题格式、hidden-test、外部数据与交付合同；
- `/metric-attestation`：GT policy/split/model/runtime/evaluator hash 指标证明；
- `/delivery-check`：Windows NVIDIA onedir 黑盒验收；
- `beekeeping-competition-workflow` Skill；
- 默认不自动 format/autofix，排除原始视频、训练数据、权重、结果和交付物。

关键边界：原始比赛视频只读；按视频/片段切分，禁止相邻帧随机泄漏；Mac 检查、AutoDL GPU 评测和 Windows 黑盒验收必须明确区分。

## 更新策略

```bash
# 默认只检查实际安装是否与锁一致
./update.sh

# 重新同步到仓库锁，不解析 latest
./update.sh --apply
```

本仓库不会自动更新 Pi core、Extension 或 MCP。更新流程应当是：

1. 在分支中修改精确版本；
2. 审查 package 来源和变更；
3. 在临时 HOME 及真实机器验证；
4. 运行 npm audit、MCP 连接和项目 smoke checks；
5. commit/push；
6. 再运行 `./update.sh --apply`。

旧版的 `com.jacky1n7.pi-config-update` 每 6 小时自动更新任务会在 apply 时卸载删除。`install-auto-update.sh` 现只解释新的显式更新策略。

## 回滚

apply 输出会打印 backup transaction，例如：

```text
~/.local/state/pi-config/backups/20260825T170000-global
```

先预览，再应用回滚：

```bash
./scripts/rollback.sh ~/.local/state/pi-config/backups/<transaction>
./scripts/rollback.sh ~/.local/state/pi-config/backups/<transaction> --apply
```

回滚仅恢复 transaction 清单中的路径，不删除无关 package、Prompt、Skill 或 MCP server。

## 安全与验证

```bash
# 仓库 JSON、Skill frontmatter、版本 pin、凭据文件检查
./scripts/check.sh

# Shell/Python 语法
bash -n install.sh update.sh install-auto-update.sh scripts/*.sh
python3 -m py_compile scripts/pi_config.py

# 实际安装漂移
./scripts/check.sh --installed --profile jacky

# 两个重点项目与模板的漂移
./scripts/check-project.sh plant-geometry-phenotyping-lab ~/plant-geometry-phenotyping-lab
./scripts/check-project.sh smart-beekeeping-challenge-cup ~/挑战杯智慧养蜂项目
```

第三方 Extension 具有当前用户权限；npm audit 为 0 不等于代码无恶意。新增 package 仍应通过 Pi Marketplace 审计和人工确认。MCP 使用精确命令版本，不存储 credential。

## 设计依据

参见 [`docs/research-sources.md`](docs/research-sources.md)。主要依据包括 Pi 官方文档、[AGENTS.md](https://agents.md/)、OpenAI Codex AGENTS 指南、PyTorch/pytest/Ruff、DVC/MLflow、MCP 安全规范和 GitHub 大文件指南。

## License

MIT
