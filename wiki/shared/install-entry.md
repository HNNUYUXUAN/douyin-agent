---
{
  "type": "Runbook",
  "title": "Install with an agent / 通过 Agent 安装",
  "description": "Install with an agent / 通过 Agent 安装 — douyin-agent operational knowledge",
  "tags": [
    "douyin-agent",
    "shared",
    "install-entry"
  ],
  "status": "active",
  "generated": {
    "by": "douyin-agent/2.5.0",
    "at": "2026-11-05T02:27:48.555869+00:00"
  },
  "sources": [
    {
      "resource": "https://github.com/GoogleCloudPlatform/knowledge-catalog/blob/62432a095456147ee71e70ac6e4dc0d2dea3ac30/okf/SPEC.md"
    }
  ],
  "applicability": {
    "skill": "2.5.x",
    "host": "capability-detected; see body for measured versions"
  },
  "verification_scope": "Documentation reviewed; runtime acceptance is recorded separately."
}
---

# Install with an agent / 通过 Agent 安装

中文：将仓库链接交给具备本地文件、终端及浏览器连接能力的 Codex 或 WorkBuddy 桌面宿主，并说：

> 请从这个仓库安装 douyin-agent，选择合适的工作区，检查依赖，并带我完成浏览器与 Agent Plan 的首次配置。

English: Give this repository link to a Codex or WorkBuddy desktop host with local file, terminal and connected-browser capabilities:

> Install douyin-agent from this repository, choose a workspace, check dependencies, and guide me through browser and Agent Plan setup.

- [中文安装指南](../zh-CN/operations/install.md)
- [English installation guide](../en/operations/install.md)
- [操作索引 / Operation index](../../docs/agent/index.json)

## New device / 全新设备

Only WorkBuddy and its browser connector installed? Start with [中文从零引导](../zh-CN/bootstrap/first-run.md) / [English zero-start guide](../en/bootstrap/first-run.md). The guides cover source acquisition without Git/Python, Conda and FFmpeg preparation, explicit WorkBuddy installation target, browser checks, local Key entry, first task and clean-device acceptance.

WorkBuddy must use `-TargetHost workbuddy` / `--host workbuddy`, or an explicitly verified skill directory. The default remains Codex for compatibility. The new-install user-level WorkBuddy location is `USER_HOME/.workbuddy/skills/douyin-agent`; verify actual client discovery.

## Agent procedure / Agent 执行顺序

1. Read `AGENTS.md` and the installation guide in the user's language. Resolve the repository root from actual downloaded files; never reuse an author's machine paths. Inspect the existing installation before replacing it.
2. Use the official repository linked below. Choose a writable short workspace, suggesting `D:\douyin-agent` only when D: exists. Choose the host's actual skill directory separately from the workspace. Reuse an existing supported Conda installation; missing dependencies follow the guide.
3. Detect the selected PowerShell 5.1/7 or Git Bash executable/version, reusing available system or host-bundled tools. From the repository root use the public installer, replacing both example paths with the detected choices. Optionally pass `-Conda CONDA_EXE` to select an existing installation:

```powershell
./install.ps1 -Workspace 'D:\douyin-agent' -SkillDir 'C:\Users\YOUR_USER\.codex\skills\douyin-agent'
```

Git Bash equivalent / Git Bash 等价入口：

```bash
bash ./install.sh --workspace '/d/douyin-agent' --skill-dir '/c/Users/YOUR_USER/.codex/skills/douyin-agent'
```

Use `--conda CONDA_EXE` to select Conda in Git Bash. Both shells call the shared Python installer using Conda base Python 3.10+ and prepare an isolated Python 3.12 runtime. Resolve relative paths from the user's current shell directory. / 两种终端共用安装核心，复用 Conda；相对路径以当前终端目录为准。

4. Read the installer result and use its actual Python/skill paths. Run `onboard --check` through `scripts/da.py`. Follow [中文首次使用](../zh-CN/operations/onboarding.md) / [English onboarding](../en/operations/onboarding.md) for the host checks and pages to open. Local checks never imply that browser access, a subscription or cloud calls have succeeded.
5. User completes browser permissions, login, purchases and local Key entry. Record observed non-sensitive readiness using `onboard --record FILE`; show only what remains unresolved. Run a real sample only after its usage preview is covered by user authorization.
6. Confirm the host can discover the installed skill. If the current host requires refresh/restart, follow its actual UI. Record whether testing used the existing conversation or a fresh independent chat; do not equate the two.

步骤摘要：读指南 → 核对来源和已有安装 → 选工作区及技能目录 → 执行安装 → 只读预检 → 打开所需页面并等待用户完成配置 → 记录实际结果 → 在用量授权内验证样例。

## Repository addresses / 仓库地址

- GitHub: https://github.com/HNNUYUXUAN/douyin-agent
- GitCode: https://gitcode.com/yuxuan6426/douyin-agent

Use one source for a given installation and record its version/commit. Do not silently mix files across mirrors. This is a Windows-first workflow; another OS or host requires its own validation. No subscription purchase or cloud request is implied by installing the skill.
