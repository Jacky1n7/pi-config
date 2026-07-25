#!/usr/bin/env bash
# 一键安装我的 Pi 配置：19 个插件 + 2 个 MCP server
# 不含供应商/模型/key —— 那些请用 `pi config` 自行配置
set -euo pipefail

echo "📦 安装 17 个 Pi 插件包..."
PACKAGES=(
	pi-subagents
	pi-mcp-adapter
	pi-web-access
	pi-lens
	context-mode
	pi-hermes-memory
	@juicesharp/rpiv-todo
	@narumitw/pi-statusline
	pi-marketplace
	@narumitw/pi-github-pr
	@narumitw/pi-plan-mode
	@narumitw/pi-goal
	pi-playwright
	pi-simplify
	@firstpick/pi-prompts-git-pr
	@firstpick/pi-skill-deep-research
	@victor-software-house/pi-curated-themes
)

for pkg in "${PACKAGES[@]}"; do
	echo "  → pi install npm:$pkg"
	pi install "npm:$pkg" || echo "    ⚠️  安装失败: $pkg（可稍后重试）"
done

echo ""
echo "🔌 配置 MCP servers..."
MCP_DIR="$HOME/.config/mcp"
MCP_FILE="$MCP_DIR/mcp.json"
mkdir -p "$MCP_DIR"

# 合并而非覆盖：保留已有的 server
if [ -f "$MCP_FILE" ]; then
	echo "  检测到已有 $MCP_FILE，将合并新 server..."
	node -e '
    const fs = require("fs");
    const existing = JSON.parse(fs.readFileSync(process.argv[1],"utf8"));
    const incoming = JSON.parse(fs.readFileSync(process.argv[2],"utf8"));
    existing.mcpServers = Object.assign({}, existing.mcpServers||{}, incoming.mcpServers||{});
    fs.writeFileSync(process.argv[1], JSON.stringify(existing,null,2)+"\n");
    console.log("  ✓ 已合并 MCP server:", Object.keys(existing.mcpServers).join(", "));
  ' "$MCP_FILE" "$(dirname "$0")/mcp.json"
else
	cp "$(dirname "$0")/mcp.json" "$MCP_FILE"
	echo "  ✓ 已写入 $MCP_FILE"
fi

echo ""
echo "✅ 安装完成！"
echo ""
echo "⚠️  下一步（本脚本不做）："
echo "   1. 用 \`pi config\` 配置你自己的 provider 和 API key"
echo "   2. chrome-devtools MCP 需要本地二进制，按 mcp.json 里的路径安装"
echo "   3. 重启 pi 使所有插件/MCP 生效"
