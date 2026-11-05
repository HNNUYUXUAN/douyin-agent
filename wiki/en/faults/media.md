---
{
  "type": "Runbook",
  "title": "Media identity, sampling and cleanup faults",
  "description": "Media identity, sampling and cleanup faults",
  "tags": [
    "media",
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

# Media identity, sampling and cleanup faults

Trigger: absent tail frame, cleanup path mismatch, wrong part/image order or capture blocked by policy. Scope: acquired task media; parser routing stays in force.
Preconditions: inspect acquisition receipt, hashes, ownership, originals and native timeline. Playback completion does not prove file integrity.
Procedure: sample within effective video-stream time. Tail-frame absence can degrade only after full decode passes; middle decode failures remain errors. Do not trim originals to manufacture success. Bilibili identity uses BV+part and separate dynamic identity; resolve av/shortlinks through user-browser pages. Count original images, not collage regions.
Normalize Windows path representations while retaining hash/ownership/reparse guards. Inspect exact cleanup_pending errors rather than deleting whole job/cache trees. Preserve import originals/unknown downloads. Preserve imported ZIPs and verify extracted copies by manifest.
Verify capture independently. Use the capture branch for host failures; do not weaken system policy when Add-Type is blocked. If necessary and host-permitted, existing FFmpeg may capture only task-public regions with ownership records, never credentials.
Success: verified identity/integrity and original-frame/image review; retire only owned media, keeping MD/JSON and unresolved ledgers.
Bounds: one cause-specific recheck, no repeated completed paid analysis merely to rewrite reports. Empty ASR does not imply silence.
Stop/resume: follow [workflow](../operations/workflow.md) and [recovery](../operations/recovery.md); preserve exact cleanup/decode errors for handoff.
