---
{
  "type": "Runbook",
  "title": "Maintenance acceptance: clean-device matrix",
  "description": "Maintenance acceptance: clean-device matrix",
  "tags": [
    "acceptance",
    "maintenance",
    "clean-test"
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

# Maintenance acceptance: clean-device matrix


## Trigger and scope
Read only for explicitly requested maintenance acceptance. Normal setup ends at configuration, without this matrix. Recipient devices install/debug/test/return evidence; only the maintainer modifies source/releases.
## Preconditions
Complete setup and reuse valid installation/configuration/evidence. Do not reset a device or reinstall dependencies to manufacture a clean start. Missing Key waits for local entry. Distinguish real clean-device, same-device relocation and fixtures.
## Procedure
1. Select explicitly scoped first/repeat/upgrade/interruption cases and actually installed terminals. Mark absent cases untested instead of installing another shell.
2. Offline suite: `PYTHON SKILL/scripts/test_all.py --workspace WORKSPACE`. Bridge/source-fetch changes also run the PS5/PS7 fixtures required by repository AGENTS.
3. Verify actual Chrome/Edge availability, explicit-instance failure, IAB exclusion, logged-in single work tab and logged-out/unknown login+work tabs. Never terminate user browsers.
4. Simulate missing Key only in isolation, preserving main credentials. Verify waiting progress with no subsequent media/cloud requests; after local entry setup finishes without a sample.
5. Work validation requires separate explicit start with mode/scope/usage authorization. Record acquisition, integrity, understanding, original review and cleanup separately; never resubmit pending calls.
6. User must actually open a fresh chat for discovery validation. Give the verifier only the candidate folder and ordinary install instruction, without author history or expected pass answers. Record host/model versions.
## Success, bounds and handoff
Each result has time/evidence/scope. Supply original issue IDs rather than asking recipients to reconstruct them. Keep unavailable checks pending. Finish after proportionate affected checks; do not repeat unchanged tests. Return ordinary directories without credentials, original media or private logs.
