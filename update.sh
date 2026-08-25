#!/usr/bin/env bash
# 更新本仓库管理的 Pi 扩展；不自动升级 Pi 主程序，以保留汉化。
set -euo pipefail

PI_AGENT_DIR="${PI_CODING_AGENT_DIR:-$HOME/.pi/agent}"
export PATH="${PI_AUTO_UPDATE_PATH:-$HOME/.npm-global/bin:$HOME/.local/bin:/opt/homebrew/bin:/usr/local/bin:/usr/bin:/bin:/usr/sbin:/sbin}"

for command_name in pi npm; do
	if ! command -v "$command_name" >/dev/null 2>&1; then
		echo "✗ 缺少必需命令: $command_name" >&2
		exit 1
	fi
done

echo "[$(date '+%Y-%m-%d %H:%M:%S')] 开始更新 Pi 扩展"
pi update --extensions --no-approve

if npm install-scripts --help >/dev/null 2>&1; then
	(
		cd "$PI_AGENT_DIR/npm"
		npm install-scripts approve @ast-grep/cli better-sqlite3 context-mode fsevents
	)
fi

echo "[$(date '+%Y-%m-%d %H:%M:%S')] Pi 扩展已是当前最新版"
