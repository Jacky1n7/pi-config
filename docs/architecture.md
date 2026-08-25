# 架构与所有权

`manifest/packages.json` 是 Pi package 锁定版本的唯一来源；`config/mcp/servers.json` 是 MCP server 锁定命令的唯一来源。`config/pi/` 只管理非密钥设置，`global/` 管理全局 AGENTS/Prompts/Skills，`templates/` 管理两个重点项目的项目级工作流。

安装器只拥有明确列出的目标文件或 JSON 键，不读取、复制或提交 `auth.json`、provider credential、session、memory、cache、日志及任意真实 MCP env/header/token。

全局应用和项目模板应用都会先备份到 `${XDG_STATE_HOME:-~/.local/state}/pi-config/backups/`，目录权限为 `0700`、清单为 `0600`。写入采用临时文件 + `os.replace`。回滚按 transaction 只恢复该次记录的路径。

旧版每 6 小时运行 `pi update --all` 的 LaunchAgent 会在全局 apply 时卸载并删除。升级改为：更新 manifest 锁 → 审查/验证 → commit → `./update.sh --apply`。
