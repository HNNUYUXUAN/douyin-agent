---
{
  "type": "Runbook",
  "title": "Conda verification, wait and partial installation",
  "description": "Conda verification, wait and partial installation",
  "tags": [
    "conda",
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

# Conda verification, wait and partial installation

Trigger: missing Conda, installer returning early, partial destination. Scope: official Windows x64 Miniconda installers.
Preconditions: discover existing Conda first. Obtain a fixed official installer and record SHA256. Compare an official digest; if unavailable, disclose that and require Valid Anaconda Authenticode. Stop on provenance/hash/signature failures.
Procedure: review scripts/install-conda.ps1, then run `./scripts/install-conda.ps1 -Workspace ABS_ROOT -Installer ABS_EXE -Sha256 RECORDED_HASH` within one host-command lifetime. Destination is workspace tools/miniconda3, without spaces; JustMe, no global PATH/Python registration. Users handle licensing/system prompts.
The wrapper starts hidden, reports progress and waits for actual Conda/Python readiness for up to 900 seconds. Parent exit alone is not readiness. Keep the original host command alive and observe its task handle instead of starting duplicate installation.
Reuse a complete existing destination; refuse to overwrite an incomplete one. Timeout preserves process/logs. Check whether the original installer is active. No automatic deletion: cleanup requires verified absolute paths, task-created ownership and no user content.
Success: successful installer exit plus conda --version and base Python>=3.10, or verified existing reuse.
Bounds: one install; at most one corrected rerun after new evidence and no active original process. Do not repeatedly delete/reinstall partial destinations.
Stop/resume: hand off signature/hash failures. Resume from preserved state on timeout; never substitute another runtime by trial and error.
