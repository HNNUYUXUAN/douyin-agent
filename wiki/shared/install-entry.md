---
{
  "type": "Runbook",
  "title": "Install and configure / 安装与配置",
  "description": "Install and configure / 安装与配置",
  "tags": [
    "install",
    "setup",
    "gate"
  ],
  "status": "stable",
  "generated": {
    "by": "douyin-agent/2.5.1",
    "at": "2026-11-05T09:57:06.630627+00:00"
  },
  "sources": [
    {
      "resource": "https://github.com/GoogleCloudPlatform/knowledge-catalog/blob/62432a095456147ee71e70ac6e4dc0d2dea3ac30/okf/SPEC.md"
    }
  ],
  "applicability": {
    "skill": "2.5.1 candidate",
    "host": "Windows x64; recheck current host capabilities"
  },
  "verification_scope": "Candidate implementation; fixture, local and recipient results are recorded separately."
}
---

# Install and configure / 安装与配置


Give the repository or candidate ordinary directory to your desktop agent. Say: “Install and configure douyin-agent on this device. Finish configuration before starting any real works.”

将仓库链接或候选普通目录交给桌面 Agent：“请安装并配置 douyin-agent，配置完成后收尾，作品等我另行开工。”

Read repository AGENTS.md, then the complete current-language setup pack: [中文](../zh-CN/bootstrap/first-run.md) / [English](../en/bootstrap/first-run.md). Default is ordinary setup, not maintenance acceptance. Inspect actual existing paths, source/version and receipts first. Use one source/commit without mixing mirrors.

Windows preflight requires no Python: `scripts/preflight.ps1 -Workspace ABS_WORKSPACE -TargetHost workbuddy`. It returns terminal, dependency/receipt status and required documents. Use returned Git Bash → PowerShell 7 → Windows PowerShell 5.1 for normal commands. Follow [中文安装](../zh-CN/operations/install.md) / [English install](../en/operations/install.md).

WorkBuddy installation must pass --host workbuddy / -TargetHost workbuddy; default new skill directory is USER_HOME/.workbuddy/skills/douyin-agent. Codex uses --host codex. Existing matching receipts take precedence. Workspace, source, skill and host conversation folders are distinct. Never copy author paths blindly.

After installation, use returned Python/skill paths with `onboard --check --flow setup --host workbuddy --observed CURRENT_JSON`. Host verifies skill discovery and current Chrome/Edge DOM/capture. Missing Key stops until local entry. Finish at local configuration; real service remains unverified. No automatic sample, session, download or paid request.

Ordinary setup does not run repeat/upgrade/interruption/full tests. Only explicit maintenance enters [中文验收](../zh-CN/bootstrap/clean-test.md) / [English acceptance](../en/bootstrap/clean-test.md). Missing or failed capabilities route to the exact manual; preserve config and evidence. A fresh-chat invocation must be actually observed before claiming it passed.

Candidate v2.5.1 is awaiting recipient verification. Install the user-specified immutable remote commit or supplied ordinary directory; do not fetch a nonexistent release tag or silently use the default older release. Public repositories: [GitHub](https://github.com/HNNUYUXUAN/douyin-agent), [GitCode](https://gitcode.com/yuxuan6426/douyin-agent).
