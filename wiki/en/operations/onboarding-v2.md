---
{
  "type": "Runbook",
  "title": "First use and configuration recovery",
  "description": "First use and configuration recovery — douyin-agent operational knowledge",
  "tags": [
    "douyin-agent",
    "en",
    "operations",
    "onboarding"
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

# Cross-browser receipts

## Cross-browser v2 receipts

`onboard --record FILE` still accepts v1. v2 retains `checks` and optionally adds `browser_observations` and `platform_bindings`. Use actual timezone-aware timestamps and clean public URLs or existing workspace MD/JSON evidence. Store opaque connection/tab IDs without account/Profile names. New checks include bilibili_access, search_available, file_save. Receipts record host observations rather than executing browser actions.

[v2 example](../../../docs/agent/examples/onboard-v2.json) · [Selection / 选择](browser-selection.md)
