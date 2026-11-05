---
{
  "type": "Runbook",
  "title": "Setup checks and current host observations",
  "description": "Setup checks and current host observations",
  "tags": [
    "onboard",
    "setup",
    "record",
    "skill_discovery",
    "observed",
    "key"
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

# Setup checks and current host observations


## Fixed entry
Read the [setup pack](../bootstrap/first-run.md) completely. Ordinary setup configures only; use awaits explicit start; acceptance is maintenance only. Missing Key stops execution until local entry; completion never launches a sample.
## Command
Use actual installer paths:
`PYTHON SKILL/scripts/da.py --workspace WORKSPACE onboard --check --flow setup --host workbuddy --language en --observed CURRENT_JSON`
Without --observed, output includes local checks and historical suggestions, requiring current host observations instead of reusing old passes. --browser-id OPAQUE_ID pins the user-selected instance; failure routes to connection recovery. For Codex use --host codex.
Output contains one next_action, required_docs, blocking_reasons, waiting_for, phase and setup_status. next_actions remains a single-element compatibility list. Reading paths are skill-root relative. Execute/recheck the current step; the local script does not perform host actions.
## Read-only and persistence
--check/--observed neither write, open pages nor call services. --record CURRENT_JSON persists onboarding.json, agent-context.json and minimal setup-progress.json. Do not combine record/observed. Resume from phase/evidence/next_action after live verification. Progress contains no credentials, page bodies or account data.
## Receipts
v1 (schema_version/checks) and v2 (browser_observations/platform_bindings added) remain accepted. Each check has only status/observed_at/evidence; statuses are passed|blocked|unverified|not_applicable. New skill_discovery records actual host discovery; distinguish listing vs fresh-chat invocation in referenced evidence. Use actual system timestamps and existing workspace-relative MD/JSON or clean public HTTPS evidence. Do not import a full acceptance template: extract observed checks, map browser_bridge to browser_connection, keep installation/cleanup in the acceptance table.
v2 still has four capabilities: connection/dom/screenshot/file_save. Optional host_capabilities stores actual host inventory names; WorkBuddy platform selection requires user_tabs, with missing legacy evidence reobserved. family=chrome|edge|other and kind=extension|iab|cdp; only Chrome/Edge user extensions qualify for platforms.
CURRENT_JSON must reflect current observations, not copied old files with refreshed timestamps. The script validates format/provenance, not whether a host actually performed actions.
## Outcome and stop
When prerequisites, matching installation receipt, skill discovery, user-browser DOM/screenshot and local Key pass, return finish_setup. Cloud fields stay false; report local configuration completed and real service unverified. No paid sample. Probe platform login/file saving only for the subsequent start scope.
Resolve prerequisites through routed manuals, browser failures through recovery, and missing Key by waiting. After local entry check once, remaining waiting if still missing.
## Example
[v2 receipt](../../../docs/agent/examples/onboard-v2.json) is illustrative and requires real observations. Use [conditional login tabs](browser-selection.md); never copy example passed values as evidence.
