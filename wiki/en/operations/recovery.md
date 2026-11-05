---
{
  "type": "Runbook",
  "title": "Recovery, cleanup and migration",
  "description": "Recovery, cleanup and migration — douyin-agent operational knowledge",
  "tags": [
    "douyin-agent",
    "en",
    "operations",
    "recovery"
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


# Recovery, cleanup and migration

[中文](../../zh-CN/operations/recovery.md) · [Index](../../../docs/agent/index.json)

## Applicable intent

Diagnose environment/acquisition/request/review/cleanup failures, read text after cleanup, or migrate historical jobs.

## Prerequisites

The actual workspace and job records are readable; preserve their current state first. Unresolved calls cannot be unlocked by retries or ledger edits, and active-process protection remains in force.

## Minimum inputs

Target job/plan and symptoms. Request issues need the original plan/job/cache_id and available platform evidence; missing fields stay unknown.


[Continue / 继续阅读](recovery-part2.md)

[Continue / 继续阅读](recovery-part3.md)
