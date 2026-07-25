# My Pi Coding Agent Setup

> 分享我的 [Pi](https://pi.dev)（开源终端 AI 编码代理）配置：**19 个插件 + 38 个全局 Skill + 2 个 MCP server**。
> 不含供应商 / 模型 / API key —— 那些因人而异且含密钥，无法照搬。

## 这是什么

一份可直接复刻的 Pi 配置，包含：

- **19 个插件**：子代理编排、代码智能、上下文管理、Web 浏览、安全审计全家桶等
- **38 个全局 Skill**：随包安装即处处可用，与项目无关
- **2 个 MCP server**：`context7`（实时文档）、`chrome-devtools`（浏览器控制）

## 一键安装

```bash
bash install.sh
```

脚本会：安装 19 个 npm 插件包 → 合并 MCP 配置到 `~/.config/mcp/mcp.json` → 提示你手动填回自己的 provider/key。

> 需要 `pi` 和 `node` 已安装。

## 内容

| 文件 | 说明 |
| --- | --- |
| `install.sh` | 一键安装脚本 |
| `config.json` | 机器可读的完整配置（plugins / globalSkills / mcpServers / UI / tools） |
| `mcp.json` | MCP server 配置（可直接放到 `~/.config/mcp/mcp.json`） |
| `README.md` | 本文件 |

## 配置亮点

- **安全审计能力拉满**：`@vigolium/piolium` 提供 20 个安全 skill（audit / semgrep / codeql / code-reviewer / vuln-report / variant-analysis / wooyun-legacy / zeroize-audit …）
- **省 token**：`context-mode` 把大输出走沙箱 + FTS5 知识库；工具列表精简，按需唤起
- **多代理编排**：`pi-subagents` 支持 single / chain / parallel / async / forked-context
- **色盲友好主题**：`github-dark-colorblind`，Thinking 级别 `high`

## 不会包含的内容

- 供应商（provider）配置
- 模型列表
- API key / 密钥

这些请用 `pi config` 自行配置。

## License

MIT
