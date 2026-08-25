#!/usr/bin/env python3
"""Transactional installer/checker for Jacky's Pi workflow configuration."""

from __future__ import annotations

import argparse
import datetime as dt
import hashlib
import json
import os
import platform
import re
import shutil
import stat
import subprocess
import sys
import tempfile
from pathlib import Path
from typing import Any

REPO = Path(__file__).resolve().parents[1]
HOME = Path.home()
PI_AGENT = Path(os.environ.get("PI_CODING_AGENT_DIR", HOME / ".pi/agent")).expanduser()
XDG_CONFIG = Path(os.environ.get("XDG_CONFIG_HOME", HOME / ".config")).expanduser()
XDG_STATE = Path(os.environ.get("XDG_STATE_HOME", HOME / ".local/state")).expanduser()
STATE_ROOT = XDG_STATE / "pi-config/backups"
MCP_FILE = XDG_CONFIG / "mcp/mcp.json"
LENS_FILE = HOME / ".pi-lens/config.json"
LEGACY_PLIST = HOME / "Library/LaunchAgents/com.jacky1n7.pi-config-update.plist"
LEGACY_UPDATE = PI_AGENT / "bin/pi-config-update.sh"
WORKFLOW_START = "<!-- pi-config:workflow:start -->"
WORKFLOW_END = "<!-- pi-config:workflow:end -->"


def load_json(path: Path) -> Any:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        raise ValueError(f"cannot read JSON {path}: {exc}") from exc


def merge(base: dict[str, Any], incoming: dict[str, Any]) -> dict[str, Any]:
    result = dict(base)
    for key, value in incoming.items():
        if isinstance(value, dict) and isinstance(result.get(key), dict):
            result[key] = merge(result[key], value)
        else:
            result[key] = value
    return result


def atomic_text(path: Path, content: str, mode: int = 0o644) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    fd, tmp_name = tempfile.mkstemp(prefix=f".{path.name}.", dir=path.parent)
    tmp = Path(tmp_name)
    try:
        with os.fdopen(fd, "w", encoding="utf-8") as handle:
            handle.write(content)
            handle.flush()
            os.fsync(handle.fileno())
        os.chmod(tmp, mode)
        os.replace(tmp, path)
    finally:
        tmp.unlink(missing_ok=True)


def atomic_json(path: Path, value: Any) -> None:
    atomic_text(path, json.dumps(value, ensure_ascii=False, indent=2) + "\n")


def hash_path(path: Path) -> str:
    return hashlib.sha256(str(path).encode()).hexdigest()[:20]


def backup(paths: list[Path], label: str) -> Path:
    stamp = dt.datetime.now().strftime("%Y%m%dT%H%M%S%f")
    root = STATE_ROOT / f"{stamp}-{label}"
    root.mkdir(parents=True, mode=0o700)
    os.chmod(root, 0o700)
    records: list[dict[str, Any]] = []
    for path in dict.fromkeys(paths):
        exists = path.exists() or path.is_symlink()
        record: dict[str, Any] = {"path": str(path), "exists": exists}
        if exists:
            slot = root / "files" / hash_path(path)
            slot.parent.mkdir(parents=True, exist_ok=True)
            if path.is_dir() and not path.is_symlink():
                shutil.copytree(path, slot, symlinks=True)
                record["kind"] = "dir"
            else:
                shutil.copy2(path, slot, follow_symlinks=False)
                record["kind"] = "file"
            record["slot"] = str(slot.relative_to(root))
            record["mode"] = stat.S_IMODE(path.lstat().st_mode)
        records.append(record)
    atomic_json(root / "manifest.json", {"createdAt": stamp, "label": label, "records": records})
    os.chmod(root / "manifest.json", 0o600)
    return root


def restore(transaction: Path, apply: bool) -> None:
    manifest = load_json(transaction / "manifest.json")
    for record in manifest["records"]:
        path = Path(record["path"])
        print(f"{'RESTORE' if apply else 'WOULD RESTORE'} {path}")
        if not apply:
            continue
        if path.is_dir() and not path.is_symlink():
            try:
                shutil.rmtree(path)
            except FileNotFoundError:
                path.parent.mkdir(parents=True, exist_ok=True)
        else:
            path.unlink(missing_ok=True)
        if record["exists"]:
            slot = transaction / record["slot"]
            path.parent.mkdir(parents=True, exist_ok=True)
            if record["kind"] == "dir":
                shutil.copytree(slot, path, symlinks=True)
            else:
                shutil.copy2(slot, path, follow_symlinks=False)
            os.chmod(path, record["mode"])


def package_spec(item: dict[str, str]) -> str:
    return f"npm:{item['name']}@{item['version']}"


def global_targets() -> list[tuple[Path, Path]]:
    pairs = [
        (REPO / "global/AGENTS.md", PI_AGENT / "AGENTS.md"),
        (REPO / "config/pi-lens/config.json", LENS_FILE),
    ]
    for source in sorted((REPO / "global/prompts").glob("*.md")):
        pairs.append((source, PI_AGENT / "prompts" / source.name))
    source_skill = REPO / "global/skills/scientific-ml-experiment"
    pairs.append((source_skill, PI_AGENT / "skills/scientific-ml-experiment"))
    return pairs


def copy_managed(source: Path, target: Path) -> None:
    if source.is_dir():
        if target.exists():
            try:
                shutil.rmtree(target)
            except FileNotFoundError:
                target.parent.mkdir(parents=True, exist_ok=True)
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copytree(source, target)
    else:
        atomic_text(target, source.read_text(encoding="utf-8"))


def current_pi_version() -> str | None:
    if not shutil.which("pi"):
        return None
    run = subprocess.run(["pi", "--version"], text=True, capture_output=True, check=False)
    return run.stdout.strip() if run.returncode == 0 else None


def validate_node() -> None:
    if not shutil.which("node"):
        raise SystemExit("缺少 node")
    version = subprocess.check_output(["node", "--version"], text=True).strip().lstrip("v")
    try:
        parts = tuple(int(x) for x in version.split(".")[:3])
    except ValueError as exc:
        raise SystemExit(f"无法解析 Node.js 版本: {version}") from exc
    if parts < (22, 5, 0):
        raise SystemExit(f"Node.js >=22.5.0 required; found {version}")


def apply_global(args: argparse.Namespace) -> None:
    validate_node()
    manifest = load_json(REPO / "manifest/packages.json")
    desired_specs = [package_spec(item) for item in manifest["packages"]]
    settings_path = PI_AGENT / "settings.json"
    managed = [settings_path, MCP_FILE, LEGACY_PLIST, LEGACY_UPDATE]
    managed.extend(target for _, target in global_targets())
    print("Mode:", "APPLY" if args.apply else "DRY-RUN")
    pi_version = current_pi_version()
    locked_pi = manifest["piCore"]["version"]
    print("Pi core current/locked:", pi_version, locked_pi)
    if args.apply and pi_version != locked_pi:
        raise SystemExit(
            f"Pi core version mismatch: installed={pi_version}, locked={locked_pi}. "
            "Install the locked Pi core explicitly before applying configuration."
        )
    for spec in desired_specs:
        print("PACKAGE", spec)
    for source, target in global_targets():
        print("FILE", source.relative_to(REPO), "->", target)
    print("MCP", REPO / "config/mcp/servers.json", "->", MCP_FILE)
    print("Legacy unattended updater -> disabled")
    if not args.apply:
        return

    transaction = backup(managed, "global")
    print("Backup:", transaction)

    if not args.skip_packages:
        if not shutil.which("pi"):
            raise SystemExit("缺少 pi；无法安装锁定包")
        for item, spec in zip(manifest["packages"], desired_specs, strict=True):
            installed = PI_AGENT / "npm/node_modules" / item["name"] / "package.json"
            current = load_json(installed).get("version") if installed.exists() else None
            if current != item["version"]:
                subprocess.run(["pi", "install", spec], check=True)
        npm_dir = PI_AGENT / "npm"
        approval = manifest.get("installScriptApprovals", [])
        if npm_dir.exists() and approval and shutil.which("npm"):
            probe = subprocess.run(
                ["npm", "install-scripts", "--help"],
                cwd=npm_dir,
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL,
                check=False,
            )
            if probe.returncode == 0:
                subprocess.run(["npm", "install-scripts", "approve", *approval], cwd=npm_dir, check=True)

    existing = load_json(settings_path) if settings_path.exists() else {}
    defaults = load_json(REPO / "config/pi/settings.defaults.json")
    profile = load_json(REPO / f"config/pi/settings.{args.profile}.json") if args.profile != "none" else {}
    configured = merge(merge(existing, defaults), profile)
    configured["packages"] = desired_specs
    atomic_json(settings_path, configured)

    existing_mcp = load_json(MCP_FILE) if MCP_FILE.exists() else {}
    incoming_mcp = load_json(REPO / "config/mcp/servers.json")
    existing_mcp["mcpServers"] = merge(existing_mcp.get("mcpServers", {}), incoming_mcp["mcpServers"])
    atomic_json(MCP_FILE, existing_mcp)

    for source, target in global_targets():
        copy_managed(source, target)

    if platform.system() == "Darwin" and LEGACY_PLIST.exists() and shutil.which("launchctl"):
        subprocess.run(
            ["launchctl", "bootout", f"gui/{os.getuid()}/com.jacky1n7.pi-config-update"],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
            check=False,
        )
    LEGACY_PLIST.unlink(missing_ok=True)
    LEGACY_UPDATE.unlink(missing_ok=True)
    print("Applied. Run /reload or restart Pi.")


def replace_workflow_block(existing: str, block: str) -> str:
    wrapped = f"{WORKFLOW_START}\n{block.strip()}\n{WORKFLOW_END}"
    pattern = re.compile(re.escape(WORKFLOW_START) + r".*?" + re.escape(WORKFLOW_END), re.S)
    if pattern.search(existing):
        return pattern.sub(wrapped, existing)
    return existing.rstrip() + "\n\n" + wrapped + "\n"


def apply_project(args: argparse.Namespace) -> None:
    root = Path(args.path).expanduser().resolve()
    template = REPO / "templates" / args.template
    if not (root / ".git").exists():
        raise SystemExit(f"不是 Git 仓库: {root}")
    targets = [root / ".pi", root / ".pi-lens.json", root / "AGENTS.md"]
    print("Mode:", "APPLY" if args.apply else "DRY-RUN")
    print("Template:", args.template, "->", root)
    for target in targets:
        print("PROJECT FILE", target)
    if not args.apply:
        return
    transaction = backup(targets, f"project-{args.template}")
    print("Backup:", transaction)
    source_pi = template / ".pi"
    target_pi = root / ".pi"
    if target_pi.exists():
        shutil.copytree(source_pi, target_pi, dirs_exist_ok=True)
    else:
        shutil.copytree(source_pi, target_pi)
    copy_managed(template / ".pi-lens.json", root / ".pi-lens.json")
    agents = root / "AGENTS.md"
    current = agents.read_text(encoding="utf-8") if agents.exists() else "# Project Instructions\n"
    block = (template / "AGENTS.workflow.md").read_text(encoding="utf-8")
    atomic_text(agents, replace_workflow_block(current, block))
    print("Applied project workflow. Trust the project and run /reload in Pi.")


def check_repo() -> list[str]:
    errors: list[str] = []
    sensitive_key = re.compile(
        r"(^|[_-])(api[_-]?key|token|secret|password|authorization|cookie|credential)($|[_-])",
        re.I,
    )
    credential_assignment = re.compile(
        r"(api[_-]?key|token|client[_-]?secret|password|authorization)"
        r"\s*[=:]\s*[\"']?[A-Za-z0-9_\-/+=]{16,}",
        re.I,
    )
    forbidden_names = {"auth.json", "credentials.json", "settings.local.json"}

    def inspect_json(value: Any, relative: Path, prefix: str = "") -> None:
        if isinstance(value, dict):
            for key, child in value.items():
                dotted = f"{prefix}.{key}" if prefix else key
                if sensitive_key.search(key) and child not in ("", None, False, "<redacted>"):
                    errors.append(f"sensitive JSON value {relative}:{dotted}")
                inspect_json(child, relative, dotted)
        elif isinstance(value, list):
            for index, child in enumerate(value):
                inspect_json(child, relative, f"{prefix}[{index}]")

    for path in sorted(REPO.rglob("*")):
        if not path.is_file() or ".git" in path.parts or "__pycache__" in path.parts:
            continue
        relative = path.relative_to(REPO)
        if path.name.lower() in forbidden_names:
            errors.append(f"forbidden credential file: {relative}")
        if path.stat().st_size > 1_000_000:
            errors.append(f"oversized repository file: {relative}")
        if path.suffix == ".json":
            try:
                parsed = load_json(path)
            except ValueError as exc:
                errors.append(f"invalid JSON {relative}: {exc}")
            else:
                inspect_json(parsed, relative)
        if path.suffix in {".md", ".sh", ".py", ".json"}:
            text = path.read_text(encoding="utf-8", errors="ignore")
            if credential_assignment.search(text):
                errors.append(f"credential-like assignment: {relative}")

    manifest = load_json(REPO / "manifest/packages.json")
    seen: set[str] = set()
    for item in manifest["packages"]:
        if not re.fullmatch(r"\d+\.\d+\.\d+(?:[-+][0-9A-Za-z.-]+)?", item["version"]):
            errors.append(f"unpinned package version: {item}")
        if item["name"] in seen:
            errors.append(f"duplicate package: {item['name']}")
        seen.add(item["name"])
    for path in (REPO / "config/mcp/servers.json", REPO / "mcp.json"):
        if "@latest" in path.read_text(encoding="utf-8"):
            errors.append(f"MCP config contains @latest: {path.relative_to(REPO)}")
    for path in sorted(REPO.rglob("SKILL.md")):
        text = path.read_text(encoding="utf-8")
        valid_name = re.search(r"^name:\s*[-a-z0-9]+\s*$", text, re.M)
        valid_description = re.search(r"^description:\s*.+", text, re.M)
        if not text.startswith("---\n") or not valid_name or not valid_description:
            errors.append(f"invalid skill frontmatter: {path.relative_to(REPO)}")
    return errors


def check_installed(profile: str) -> list[str]:
    errors: list[str] = []
    manifest = load_json(REPO / "manifest/packages.json")
    settings_path = PI_AGENT / "settings.json"
    if not settings_path.exists():
        return [f"missing {settings_path}"]
    settings = load_json(settings_path)
    installed_pi = current_pi_version()
    locked_pi = manifest["piCore"]["version"]
    if installed_pi != locked_pi:
        errors.append(f"Pi core: installed={installed_pi}, locked={locked_pi}")
    desired = [package_spec(item) for item in manifest["packages"]]
    if settings.get("packages") != desired:
        errors.append("installed package specs differ from exact manifest order/pins")
    for item in manifest["packages"]:
        pkg = PI_AGENT / "npm/node_modules" / item["name"] / "package.json"
        current = load_json(pkg).get("version") if pkg.exists() else None
        if current != item["version"]:
            errors.append(f"package {item['name']}: installed={current}, locked={item['version']}")
    desired_settings = merge(load_json(REPO / "config/pi/settings.defaults.json"), load_json(REPO / f"config/pi/settings.{profile}.json") if profile != "none" else {})
    def compare_subset(actual: dict[str, Any], expected: dict[str, Any], prefix: str = "") -> None:
        for key, value in expected.items():
            dotted = f"{prefix}.{key}" if prefix else key
            if isinstance(value, dict):
                if not isinstance(actual.get(key), dict):
                    errors.append(f"missing settings object {dotted}")
                else:
                    compare_subset(actual[key], value, dotted)
            elif actual.get(key) != value:
                errors.append(f"settings drift {dotted}: {actual.get(key)!r} != {value!r}")
    compare_subset(settings, desired_settings)
    for source, target in global_targets():
        if not target.exists():
            errors.append(f"missing managed target {target}")
        elif source.is_file() and source.read_bytes() != target.read_bytes():
            errors.append(f"managed file drift {target}")
    if MCP_FILE.exists():
        actual = load_json(MCP_FILE).get("mcpServers", {})
        expected = load_json(REPO / "config/mcp/servers.json")["mcpServers"]
        for name, config in expected.items():
            if actual.get(name) != config:
                errors.append(f"MCP drift {name}")
    else:
        errors.append(f"missing {MCP_FILE}")
    if LEGACY_PLIST.exists() or LEGACY_UPDATE.exists():
        errors.append("legacy unattended update-all job still installed")
    return errors


def cmd_check(args: argparse.Namespace) -> None:
    errors = check_repo()
    if args.installed:
        errors.extend(check_installed(args.profile))
    if errors:
        for error in errors:
            print("ERROR", error)
        raise SystemExit(1)
    print("OK repo configuration")
    if args.installed:
        print("OK installed configuration")


def cmd_check_project(args: argparse.Namespace) -> None:
    root = Path(args.path).expanduser().resolve()
    template = REPO / "templates" / args.template
    errors: list[str] = []
    for source in sorted((template / ".pi").rglob("*")):
        if not source.is_file():
            continue
        target = root / source.relative_to(template)
        if not target.exists():
            errors.append(f"missing project resource {target}")
        elif source.read_bytes() != target.read_bytes():
            errors.append(f"project resource drift {target}")
    lens_target = root / ".pi-lens.json"
    if not lens_target.exists() or lens_target.read_bytes() != (template / ".pi-lens.json").read_bytes():
        errors.append(f"project resource drift {lens_target}")
    agents = root / "AGENTS.md"
    if not agents.exists():
        errors.append(f"missing {agents}")
    else:
        expected = (template / "AGENTS.workflow.md").read_text(encoding="utf-8").strip()
        match = re.search(
            re.escape(WORKFLOW_START) + r"\n(.*?)\n" + re.escape(WORKFLOW_END),
            agents.read_text(encoding="utf-8"),
            re.S,
        )
        if not match or match.group(1).strip() != expected:
            errors.append(f"AGENTS workflow drift {agents}")
    if errors:
        for error in errors:
            print("ERROR", error)
        raise SystemExit(1)
    print(f"OK project configuration {root}")


def parser() -> argparse.ArgumentParser:
    root = argparse.ArgumentParser()
    sub = root.add_subparsers(dest="command", required=True)
    global_cmd = sub.add_parser("apply-global")
    global_cmd.add_argument("--apply", action="store_true")
    global_cmd.add_argument("--profile", choices=["jacky", "none"], default="jacky")
    global_cmd.add_argument("--skip-packages", action="store_true")
    global_cmd.set_defaults(func=apply_global)
    project = sub.add_parser("apply-project")
    project.add_argument("template", choices=["plant-geometry-phenotyping-lab", "smart-beekeeping-challenge-cup"])
    project.add_argument("path")
    project.add_argument("--apply", action="store_true")
    project.set_defaults(func=apply_project)
    check = sub.add_parser("check")
    check.add_argument("--installed", action="store_true")
    check.add_argument("--profile", choices=["jacky", "none"], default="jacky")
    check.set_defaults(func=cmd_check)
    project_check = sub.add_parser("check-project")
    project_check.add_argument(
        "template",
        choices=["plant-geometry-phenotyping-lab", "smart-beekeeping-challenge-cup"],
    )
    project_check.add_argument("path")
    project_check.set_defaults(func=cmd_check_project)
    rollback = sub.add_parser("rollback")
    rollback.add_argument("transaction", type=Path)
    rollback.add_argument("--apply", action="store_true")
    rollback.set_defaults(func=lambda args: restore(args.transaction.expanduser().resolve(), args.apply))
    return root


def main() -> int:
    args = parser().parse_args()
    args.func(args)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
