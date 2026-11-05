---
{
  "type": "Runbook",
  "title": "Observation, knowledge and session receipt faults",
  "description": "Observation, knowledge and session receipt faults",
  "tags": [
    "records",
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

# Observation, knowledge and session receipt faults

Trigger: rejected sources, future timestamps, invalid acceptance-template import, login walls without work IDs, session authorization or search problems. Scope: v1/v2 receipts and compatible 2.5.x jobs.
Preconditions: inspect actual --help, machine index and offending field. A full acceptance table is not an onboard input.
Procedure: knowledge evidence accepts existing workspace MD/JSON relative paths, bare or workspace:-prefixed, with containment checks retained. Read actual system time, not conversation estimates. Import only checks entries with status/observed_at/evidence; omit null times, keeping installation fields in the acceptance table.
Record login walls without canonical identity in session pending; never invent IDs. Authorization binds session/configuration, with legacy reads retained; never copy another session's approval. Use the fault index or `knowledge.py route --code CODE --language en`, then short search terms. Retrieval is not proof of successful repair.
Use knowledge.py record's eight-field case template, with observed symptom/action/result/evidence. Successes and failures stay local draft cases until reviewed. Use field allowlists; never dump environments, unknown clipboards, credentials, signed links, account data or raw private logs.
Success: validated real evidence can be searched again, legacy jobs remain readable, pending reservations unchanged.
Bounds: correct actual format once, then submit. Repeated failure is handed off; do not weaken validation.
Stop/resume: inspect live status and original unresolved reservations first; preserve missing/error facts and follow [recovery](../../shared/recovery-protocol.md).
