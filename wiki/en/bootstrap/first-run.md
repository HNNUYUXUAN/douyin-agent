---
{
  "type": "Runbook",
  "title": "First setup: ordered steps and stop conditions",
  "description": "First setup: ordered steps and stop conditions",
  "tags": [
    "setup",
    "first-run",
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

# First setup: ordered steps and stop conditions


## Read completely before execution

Use one language. Read this page, [dependencies](dependencies.md), the current host [WorkBuddy](workbuddy.md) or [Codex](codex.md), [browser selection](../operations/browser-selection.md), [Key setup](key.md), and [fault index](../faults/index.md) in order. Reuse unchanged content already read during this setup. docs/agent/index.json setup_flow is the machine list.

## S0 Select intent

Use setup for ordinary installation/configuration, use for normal tasks, and acceptance only for explicitly requested maintenance. Ordinary setup does not run upgrade/interruption/repeat-install matrices, full tests, multi-platform works or paid samples.

## S1 Read-only preflight

From the actual source root: `scripts/preflight.ps1 -Workspace ABS_WORKSPACE -TargetHost workbuddy` (use codex for Codex). Windows PowerShell is sufficient, without Python. Run normal installation with the returned Git Bash → PowerShell 7 → 5.1 choice. Output covers actual paths, versions, missing dependencies, receipt and reading pack. Effective write permission remains unverified until the installer performs its first write.

## S2 Prepare missing prerequisites and install

Follow [dependencies](dependencies.md), then [installation](../operations/install.md), using existing install.sh/install.ps1. Reuse receipts/configuration. Do not repeat a successful install merely to confirm it. On failure, read the matching manual and preserve the environment/receipts.

## S3 Host discovery and browser

Record actual skill discovery; distinguish current-chat and fresh-chat results. If a fresh chat cannot be opened, leave that scope pending rather than reinstalling. Verify the connected Chrome/Edge extension, DOM and a public-page screenshot. Check only necessary instances, not all five platforms. Without a selected platform, do not create platform login tabs.

## S4 Wait for Key

If missing, follow [Key setup](key.md): show the local path and official page, save waiting progress, and end execution until the user fills it locally. There is no skip option. Do not continue to work acquisition, browse sessions or model calls.

## S5 Finish configuration

Use actual installer paths: `PYTHON SKILL/scripts/da.py --workspace WORKSPACE onboard --check --flow setup --host workbuddy --observed CURRENT_JSON`. CURRENT_JSON contains current host observations; see [receipts](../operations/onboarding.md). Execute the one next_action, then recheck. Only `--record CURRENT_JSON` persists observations and setup-progress.json.

At finish_setup report “Local configuration completed; real service not yet verified”, and finish. Real works require the user's explicit start. Standing quota authorization does not start a sample.

## Resume and stop

Inspect setup-progress.json, actual receipts and missing items; obtain current host observations instead of copying old passes. Read a matched manual completely and record verified outcomes. Unknown faults follow [handoff](../faults/unknown.md). Track download, installation, human waiting, diagnosis and maintenance time separately; host credits and Agent Plan usage are separate, with unknown values left unknown.


Explicit preflight invocation from the actual source root: `powershell.exe -NoProfile -File ./scripts/preflight.ps1 -Workspace ABS_WORKSPACE -TargetHost workbuddy`. Substitute the actual short workspace and quote spaces; do not execute .ps1 as a Bash script. Preflight returns the complete first-read pack; subsequent onboard checks return only current-phase documents, reusing content already read.
