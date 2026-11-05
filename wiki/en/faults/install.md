---
{
  "type": "Runbook",
  "title": "Installation, terminal and source faults",
  "description": "Installation, terminal and source faults",
  "tags": [
    "install",
    "fault",
    "troubleshooting",
    "故障"
  ],
  "status": "stable",
  "generated": {
    "by": "douyin-agent/2.5.1",
    "at": "2026-11-05T09:44:27.533063+00:00"
  },
  "sources": [
    {
      "resource": "../../shared/acceptance/field-v251.md"
    },
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

# Installation, terminal and source faults

Trigger: terminal errors, native-stderr interruption, source failure, partial installs, conflicts, slow dependencies or FFmpeg missing in tests.
Scope: Windows Git Bash/PowerShell 5.1/7, skill 2.5.x. Field host 5.9.3 results apply only to the observed environment.
Preconditions: inspect preflight, receipt and last progress stage. Preserve .env/unknown files. Inspect only allowlisted variable presence, never env/set or full host configurations.
Procedure:
1. Existing Git Bash → existing PowerShell 7 → 5.1. Do not install a shell merely for preference. Discover Conda using explicit path, CONDA_EXE, PATH, workspace tools and known locations, without whole-disk scans.
2. If raw is unavailable, use the dependency guide's official API/fixed-commit codeload allowlist fallback; do not mix sources/commits.
3. PS5 `2>&1 | Tee-Object` relies on launch isolating/restoring error preference and checking native exit codes. Preserve the code/stage if it still fails; do not discard logs and blindly retry.
4. If environment exists but skill installation is incomplete, ensure no install remains active, then rerun the same command once. Reuse the environment. Hash conflicts/unknown directories stop replacement; preserve diagnostics/workspace.
5. Wait while the original pip process makes progress; do not start another install. An explicit trusted package index is process-local and recorded without credentials. --no-warn-script-location suppresses only irrelevant script-path warnings.
6. Maintenance only: `PYTHON SKILL/scripts/test_all.py --workspace WORKSPACE` configures process-local FFmpeg and checks both executables. Normal setup never runs this matrix.
Success: exit 0, matching version/paths/receipt, preserved configuration and unknown files. Local checks do not prove cloud/fresh-chat success.
Bounds: one rerun after resolving a diagnosed cause; repeated failure stops with stage, preserved resources and resume command.
Stop/resume: see [Conda](conda.md), [bridge](../operations/browser-recovery.md), or [unknown faults](unknown.md).


Additional observed fault: a PS7 parent module path may leave Get-FileHash unavailable in PS5. Windows-specific helpers explicitly import engine-local Utility/Security from PSHOME/Modules within PS5, without changing global PSModulePath. Preserve remaining module errors; do not copy PS7 modules into PS5.
