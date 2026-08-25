#!/usr/bin/env bash
# 在 macOS 上安装用户级 LaunchAgent：登录时及每 6 小时更新 Pi 主程序和扩展。
set -euo pipefail

if [ "$(uname -s)" != "Darwin" ]; then
	echo "ℹ️  自动更新 LaunchAgent 仅适用于 macOS，已跳过。"
	exit 0
fi

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
LABEL="com.jacky1n7.pi-config-update"
PLIST_DIR="$HOME/Library/LaunchAgents"
PLIST_FILE="$PLIST_DIR/$LABEL.plist"
PI_AGENT_DIR="${PI_CODING_AGENT_DIR:-$HOME/.pi/agent}"
BIN_DIR="$PI_AGENT_DIR/bin"
INSTALLED_UPDATE="$BIN_DIR/pi-config-update.sh"
LOG_DIR="$PI_AGENT_DIR/logs"
UPDATE_PATH="$HOME/.npm-global/bin:$HOME/.local/bin:/opt/homebrew/bin:/usr/local/bin:/usr/bin:/bin:/usr/sbin:/sbin"

mkdir -p "$PLIST_DIR" "$BIN_DIR" "$LOG_DIR"
install -m 755 "$SCRIPT_DIR/update.sh" "$INSTALLED_UPDATE"

node - "$PLIST_FILE" "$INSTALLED_UPDATE" "$LOG_DIR/pi-config-update.log" "$UPDATE_PATH" <<'NODE'
const fs = require("node:fs");
const [plistPath, scriptPath, logPath, updatePath] = process.argv.slice(2);
const xml = (value) => value
  .replaceAll("&", "&amp;")
  .replaceAll("<", "&lt;")
  .replaceAll(">", "&gt;")
  .replaceAll('"', "&quot;")
  .replaceAll("'", "&apos;");
const plist = `<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
  <key>Label</key>
  <string>com.jacky1n7.pi-config-update</string>
  <key>ProgramArguments</key>
  <array>
    <string>/bin/bash</string>
    <string>${xml(scriptPath)}</string>
  </array>
  <key>EnvironmentVariables</key>
  <dict>
    <key>PI_AUTO_UPDATE_PATH</key>
    <string>${xml(updatePath)}</string>
  </dict>
  <key>RunAtLoad</key>
  <true/>
  <key>StartInterval</key>
  <integer>21600</integer>
  <key>StandardOutPath</key>
  <string>${xml(logPath)}</string>
  <key>StandardErrorPath</key>
  <string>${xml(logPath)}</string>
</dict>
</plist>
`;
fs.writeFileSync(plistPath, plist);
NODE

launchctl bootout "gui/$UID/$LABEL" >/dev/null 2>&1 || true
launchctl bootstrap "gui/$UID" "$PLIST_FILE"
echo "⏱️  自动更新已启用：登录时及每 6 小时更新 Pi 主程序和扩展。"
echo "   日志：$LOG_DIR/pi-config-update.log"
