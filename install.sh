#!/usr/bin/env bash
# Pi 0.84.3 全量中文配置：17 个锁版 Pi 包 + 2 个懒启动 MCP server。
# 不读取或修改 auth.json，不覆盖已有 provider/model 配置。
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PI_AGENT_DIR="${PI_CODING_AGENT_DIR:-$HOME/.pi/agent}"
MCP_DIR="${XDG_CONFIG_HOME:-$HOME/.config}/mcp"
MCP_FILE="$MCP_DIR/mcp.json"

for command_name in pi node npm npx; do
	if ! command -v "$command_name" >/dev/null 2>&1; then
		echo "✗ 缺少必需命令: $command_name" >&2
		exit 1
	fi
done

node_major="$(node -p 'process.versions.node.split(".")[0]')"
if [ "$node_major" -lt 22 ]; then
	echo "✗ context-mode 需要 Node.js >= 22.5.0，当前为 $(node --version)" >&2
	exit 1
fi

echo "Pi: $(pi --version)"
echo "Node.js: $(node --version)"
echo "📦 安装 17 个已验证版本的 Pi 包..."
PACKAGES=(
	"pi-subagents@0.56.0"
	"pi-mcp-adapter@2.27.0"
	"pi-web-access@0.24.2"
	"pi-lens@4.1.2"
	"context-mode@1.0.169"
	"pi-hermes-memory@0.9.6"
	"@juicesharp/rpiv-todo@2.7.1"
	"@narumitw/pi-statusline@0.49.13"
	"pi-marketplace@0.1.3"
	"@narumitw/pi-github-pr@0.49.6"
	"@narumitw/pi-plan-mode@0.55.0"
	"@narumitw/pi-goal@0.54.0"
	"pi-playwright@0.1.1"
	"pi-simplify@0.2.3"
	"@firstpick/pi-prompts-git-pr@0.1.6"
	"@firstpick/pi-skill-deep-research@0.1.9"
	"@victor-software-house/pi-curated-themes@0.2.1"
)

failed_packages=()
for package_spec in "${PACKAGES[@]}"; do
	echo "  → pi install npm:$package_spec"
	if ! pi install "npm:$package_spec"; then
		failed_packages+=("$package_spec")
	fi
done

if npm install-scripts --help >/dev/null 2>&1; then
	echo ""
	echo "🛡️  启用已审核的本地功能依赖..."
	(
		cd "$PI_AGENT_DIR/npm"
		npm install-scripts approve @ast-grep/cli better-sqlite3 context-mode fsevents
	)
fi

echo ""
echo "🎨 合并 Pi 界面默认项..."
mkdir -p "$PI_AGENT_DIR"
node - "$PI_AGENT_DIR/settings.json" "$SCRIPT_DIR/settings.defaults.json" <<'NODE'
const fs = require("node:fs");
const [targetPath, defaultsPath] = process.argv.slice(2);
const existing = fs.existsSync(targetPath)
  ? JSON.parse(fs.readFileSync(targetPath, "utf8"))
  : {};
const defaults = JSON.parse(fs.readFileSync(defaultsPath, "utf8"));
fs.writeFileSync(targetPath, `${JSON.stringify({ ...existing, ...defaults }, null, 2)}\n`);
console.log(`  ✓ 已保留原配置并合并默认项: ${Object.keys(defaults).join(", ")}`);
NODE

echo ""
echo "🔌 合并 2 个 MCP server..."
mkdir -p "$MCP_DIR"
node - "$MCP_FILE" "$SCRIPT_DIR/mcp.json" <<'NODE'
const fs = require("node:fs");
const [targetPath, incomingPath] = process.argv.slice(2);
const existing = fs.existsSync(targetPath)
  ? JSON.parse(fs.readFileSync(targetPath, "utf8"))
  : {};
const incoming = JSON.parse(fs.readFileSync(incomingPath, "utf8"));
existing.mcpServers = {
  ...(existing.mcpServers || {}),
  ...(incoming.mcpServers || {}),
};
fs.writeFileSync(targetPath, `${JSON.stringify(existing, null, 2)}\n`);
console.log(`  ✓ MCP servers: ${Object.keys(existing.mcpServers).join(", ")}`);
NODE

echo ""
echo "🔎 已安装 Pi 包："
pi list

if [ "${#failed_packages[@]}" -ne 0 ]; then
	echo "" >&2
	echo "✗ 以下包安装失败：${failed_packages[*]}" >&2
	exit 1
fi

echo ""
echo "✅ 全量配置安装完成。重启 Pi 或在现有会话运行 /reload。"
