---
{
  "type": "Runbook",
  "title": "Install and upgrade",
  "description": "Install and upgrade — douyin-agent operational knowledge",
  "tags": [
    "douyin-agent",
    "en",
    "operations",
    "install"
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

# Install and upgrade

[中文](../../zh-CN/operations/install.md) · [Index](../../../docs/agent/index.json)

For a new WorkBuddy device read [zero-start](../bootstrap/first-run.md). Explicitly use `-TargetHost workbuddy` / `--host workbuddy` rather than the Codex default directory.

## Applicable intent

Install from a repository for the first time, or upgrade an existing installation and rebuild its isolated runtime.

## Prerequisites

The host has local file/terminal access and the user-selected source version. Windows is the tested baseline. Identify existing installations and prerequisites; use the official guidance below for missing parts.

## Minimum inputs

Repository source/version, a writable workspace and the host skill directory; provide the Conda executable path when selecting an existing installation explicitly. Installation does not require sharing a Key with the agent.

## Procedure

For the host agent receiving a repository link. Read [AGENTS.md](../../../AGENTS.md) first. Windows Codex is the baseline; reading the repository does not establish browser access or cloud readiness.

1. Obtain an ordinary directory from the user-selected [GitHub](https://github.com/HNNUYUXUAN/douyin-agent) or [GitCode](https://gitcode.com/yuxuan6426/douyin-agent) repository. Check `SKILL.md`, `delivery.json`, scripts and lockfiles. Record source/version and do not mix mirror contents.
2. Discover the host's actual skill directory. Keep it separate from the workspace. Suggest `D:\douyin-agent` when D: exists; otherwise choose another writable short path. New names use short ASCII. The workspace root is at most 85 characters to leave room for task paths, which must stay within 160 characters.
3. Locate and check the user-selected Windows PowerShell 5.1, PowerShell 7, or Git Bash, reusing system or host-bundled tools. Check existing Conda (base Python 3.10+) and FFmpeg/FFprobe. The installer reuses Conda and creates an isolated Python 3.12 environment. If Conda is missing, open the [official Miniconda guide](https://www.anaconda.com/docs/getting-started/miniconda/install); use the [official FFmpeg entry](https://ffmpeg.org/download.html) for media tools. Explain the missing installation step. Missing configuration must not trigger paid calls.
4. From the repository root, replace the example paths and run:

```powershell
./install.ps1 -Workspace 'D:\douyin-agent' -SkillDir 'C:\Users\YOUR_USER\.codex\skills\douyin-agent'
```

`setup.ps1 -Workspace WORKSPACE` rebuilds the runtime for an existing source copy; it does not install the skill into host discovery. Setup also accepts `-Conda CONDA_EXE` to select an existing Conda executable explicitly.


Git Bash uses the same installation core:

```bash
bash ./install.sh --workspace '/d/douyin-agent' --skill-dir '/c/Users/YOUR_USER/.codex/skills/douyin-agent'
```

Conda selection: explicit `-Conda` / `--conda` → `CONDA_EXE` → PATH → common Miniconda/Anaconda/Miniforge locations under the user directory and ProgramData. Git Bash accepts `/d/...` and Windows paths; quote spaces and use Git Bash rather than WSL Bash. Call the workspace interpreter directly; Conda activation is unnecessary.

To prepare only the environment, use `bash ./setup.sh --workspace '/d/douyin-agent' --conda '/c/PATH_TO_CONDA/Scripts/conda.exe'`; omit Conda for discovery. If device policy blocks PowerShell execution, report the specific policy so the user can follow their device-management requirements.

5. Resolve the Python executable and skill root from the installation result. Commands use `PYTHON SKILL/scripts/da.py --workspace WORKSPACE COMMAND`; quote paths with spaces.
6. Continue with [onboarding](onboarding.md): run `onboard --check`, then have the host inspect browser capabilities. A local `doctor` pass is not a real-service test.

Before upgrading, compare the previous receipt's hashes. Preserve user edits, unknown added files and `.env`; keep code rollback outside skill discovery. Do not wipe a workspace to resolve conflicts. Verify the installed version, isolated environment path and local configuration refer to the intended installation.

Verify natural-language discovery using actual host behavior; refresh when required. Record existing-chat and fresh-chat discovery separately.


Installation separates environment preparation from the file transaction. Prepared environments and newly created configuration remain after failure for repair/retry; existing `.env` is preserved. The file transaction covers skill files, retired files, the receipt, workspace.json, and agent-context.json. Failure restores prior contents; incomplete rollback is recorded in backup/recovery.json. Retired files are backed up and removed only after matching old receipt hashes; unknown user files remain. After success, both workspace records point to the actual installed skill.

## Expected outputs and success evidence

The installation receipt matches the actual skill directory/workspace, with checkable release hashes, Python path and local dependency results. Browser, cloud and natural-language discovery are verified separately, not inferred from installation.

## Stop or recovery conditions

Stop overwriting on user-edit conflicts, unknown existing directories, missing environments or out-of-bounds paths; preserve the state. Use [recovery](recovery.md) to distinguish environment and job issues.

## Next links

Continue with [onboarding](onboarding.md), then [acquisition](acquisition.md) and the [workflow](workflow.md).



Use built-in Windows PowerShell to run read-only `scripts/terminal.ps1`; it returns the preferred executable and version. Execute installation through that returned shell.
