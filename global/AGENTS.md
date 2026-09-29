# Jacky's Global Agent Workflow

本文件只放跨项目长期有效的规则；项目事实、命令、数据边界和验收条件由仓库内更具体的 `AGENTS.md` 覆盖。

## 沟通与证据

- 面向用户默认使用简体中文；代码、命令、协议字段和报错保持原文。
- 面向用户可见的计划、进度、推理摘要、决策依据和解释使用简体中文。
- 不展示或伪造模型隐藏的原始思维链；需要说明推理时，提供简洁、可验证、面向结论的中文摘要。
- 区分已验证事实、合理推断和待验证事项，不把搜索摘要、模型判断或退出码单独当作最终证据。
- 技术/API事实优先官方文档、规范和源码；时效性强或用户要求时联网核验。
- 最终汇报至少包含：变更文件、验证命令与结果、未验证项、残余风险。

## 本机环境真源

- 全局 Pi 配置（settings、AGENTS.md、APPEND_SYSTEM.md、prompts、skills、pi-lens、MCP server、扩展锁）的唯一真源是 `~/Documents/Codex/2026-08-25/pi/pi-config`。不要直接手改 `~/.pi/agent/*`：改仓库后跑 `./install.sh --apply --profile jacky`，再用 `./scripts/check.sh --installed --profile jacky` 验证；只读 drift 检查用 `./update.sh`。provider 凭据（`auth.json`、`custom-providers.json`、`models.json`）不在托管范围，属本机私有配置。
- 该仓库不锁也不降级 Pi Core：用 `./update.sh --self` 跟随最新稳定版；扩展与 MCP 使用精确版本，升级必须走「改锁 → 审查变更 → 真实环境验证 → 提交 → apply」。禁止无人值守 `pi update --all`。
- Pi Core 升级会覆盖本机中文补丁。升级后必须运行 `python3 ~/pi-zh-pi-coding-agent/pi-zh-apply.py --check`，确认 0 待处理、0 未匹配、运行入口已激活；出现未匹配时按该仓库 `docs/maintenance.md` 重生成补丁集，不得只改版本号。
- MCP server 与 Web 工具是按需生命周期：MCP 为 lazy，首次调用需启动进程（数秒延迟），pi-mcp-adapter 3.x 的工具名形如 `<server>_<tool>`；Web 工具当前配置为 eager 常驻。不要在未验证连接的情况下断言某个 server 或工具不可用。
- pi-subagents ≥0.73 的新会话默认只暴露 `subagents_enable`：需要委托时先调用它，`subagent` 才会出现在下一次模型请求里。
- 不要在 `enabledModels` / `modelThinkingLevels` 里保留本机不可用的模型（如 ChatGPT 账号下的 `openai-codex/gpt-5.6-sol`）：无扩展子进程（记忆库 consolidation、后台整理）会回落到它并全部失败。改完 `settings.json` / `hermes-memory-config.json` 必须在**新进程**里验证，当前会话仍用旧配置。

## 开工前

1. 读取当前目录及父目录的 `AGENTS.md`/`CLAUDE.md`，确认更具体规则。
2. 检查 `git status --short --branch`；不得覆盖、回滚、暂存或提交用户已有改动。
3. 找到真实入口、测试命令和 Source of Truth；不要凭目录名猜技术栈。
4. 多步骤任务使用 Todo；复杂跨域任务可用 Subagents，但同一工作树保持单一写入者。

## 工作流选择

- 普通多步骤执行：Todo。
- 只读方案协作：Plan Mode。
- 目标清晰且要求自主闭环：Goal Mode。
- 并行侦察、研究或审查：Subagents；写入默认串行。
- 有重大权衡、需要多专家交叉质询：Council。
- 不为简单任务强行套复杂编排；先明确验收，再选择最轻量的流程。

## 工具选择

- 本地事实：先读代码、测试、配置、日志和 Git 历史。
- 库/API最新文档：Context7；一般网页研究：Web Access。
- 可重复网页交互：Playwright；Console、Network、性能和 Lighthouse：Chrome DevTools。
- 大日志、测试输出、JSON和仓库统计：Context Mode，避免把原始大输出灌入上下文。
- 代码定位优先 `symbol_search → module_report → read_symbol`；需要结构搜索时再激活 AST/LSP 工具。
- Pi 扩展/配置改动后重启 Pi 或 `/reload` 才生效；改了扩展版本必须新开进程实测，不能只凭 `check.sh` 通过就宣称可用。

## 实施与验证

- 先定义验证合同：预期行为、最小检查、真实用户路径和需要返回的证据。
- 修复根因，遵循现有架构与风格；不引入无需求支撑的抽象或兜底。
- 验证按成本递增：语法/配置 → 定向测试与静态检查 → 集成/干跑 → 真实环境或完整测试。
- 修改代码后先看 LSP/诊断，再跑项目声明的命令；没有配置的 typecheck、构建或测试不得自行宣称通过。
- 提交、推送、发布、部署、上传数据和外部评论只在用户授权范围内执行。

## 数据、科研与安全

- 原始数据、密钥、凭据、模型权重、训练产物和大型二进制默认不进入 Git。
- 对科学/ML结论记录代码版本、脏工作树状态、数据/切分清单、配置、随机种子、环境、硬件、指标口径和产物哈希。
- 禁止用测试集、隐藏集或相邻帧泄漏调参；指标必须绑定数据口径和评测脚本版本。
- 执行删除、清理、重置、批量格式化、迁移、训练、远端操作前检查影响范围；忽略目录中的文件同样可能是不可恢复资产。
- 第三方 Skill、MCP、Extension 视为可执行供应链依赖：先审计、锁版本、最小权限；不得提交真实 token/env/header。

## 记忆与沉淀

- 用户偏好、稳定项目约定和工具坑写入持久记忆；临时进度只放 Todo。
- 可复用流程沉淀为 Skill；一次性任务不要制造长期噪声。
- 全局规则保持短而稳定，项目细节放项目 `AGENTS.md`，任务参数放 Prompt。
