# Install with an agent / 通过 Agent 安装

中文：将仓库链接交给具备本地文件、终端及浏览器连接能力的 Codex 桌面宿主，并说：

> 请从这个仓库安装 douyin-agent，选择合适的工作区，检查依赖，并带我完成浏览器与 Agent Plan 的首次配置。

English: Give this repository link to a Codex desktop host with local file, terminal and connected-browser capabilities:

> Install douyin-agent from this repository, choose a workspace, check dependencies, and guide me through browser and Agent Plan setup.

- [中文安装指南](docs/agent/zh-CN/install.md)
- [English installation guide](docs/agent/en/install.md)
- [操作索引 / Operation index](docs/agent/index.json)

## Agent procedure / Agent 执行顺序

1. Read `AGENTS.md` and the installation guide in the user's language. Resolve the repository root from actual downloaded files; never reuse an author's machine paths. Inspect the existing installation before replacing it.
2. Use the official repository linked below. Choose a writable short workspace, suggesting `D:\douyin-agent` only when D: exists. Choose the host's actual skill directory separately from the workspace. Reuse an existing supported Conda installation; missing dependencies follow the guide.
3. From the repository root use the public installer, replacing both example paths with the detected choices. Optionally pass `-Conda CONDA_EXE` to select an existing installation:

```powershell
./install.ps1 -Workspace 'D:\douyin-agent' -SkillDir 'C:\Users\YOUR_USER\.codex\skills\douyin-agent'
```

4. Read the installer result and use its actual Python/skill paths. Run `onboard --check` through `scripts/da.py`. Follow [中文首次使用](docs/agent/zh-CN/onboarding.md) / [English onboarding](docs/agent/en/onboarding.md) for the host checks and pages to open. Local checks never imply that browser access, a subscription or cloud calls have succeeded.
5. User completes browser permissions, login, purchases and local Key entry. Record observed non-sensitive readiness using `onboard --record FILE`; show only what remains unresolved. Run a real sample only after its usage preview is covered by user authorization.
6. Confirm the host can discover the installed skill. If the current host requires refresh/restart, follow its actual UI. Record whether testing used the existing conversation or a fresh independent chat; do not equate the two.

步骤摘要：读指南 → 核对来源和已有安装 → 选工作区及技能目录 → 执行安装 → 只读预检 → 打开所需页面并等待用户完成配置 → 记录实际结果 → 在用量授权内验证样例。

## Repository addresses / 仓库地址

- GitHub: https://github.com/HNNUYUXUAN/douyin-agent
- GitCode: https://gitcode.com/yuxuan6426/douyin-agent

Use one source for a given installation and record its version/commit. Do not silently mix files across mirrors. This is a Windows-first workflow; another OS or host requires its own validation. No subscription purchase or cloud request is implied by installing the skill.
