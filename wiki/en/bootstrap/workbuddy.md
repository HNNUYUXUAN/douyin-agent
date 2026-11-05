---
{
  "type": "Runbook",
  "title": "WorkBuddy host integration",
  "description": "WorkBuddy host integration — douyin-agent operational knowledge",
  "tags": [
    "douyin-agent",
    "en",
    "bootstrap",
    "workbuddy"
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

# WorkBuddy host integration

New installs use the current user `.workbuddy/skills/douyin-agent`; preserve existing receipt paths. Record runtime workspace separately from host session directory. Mark discovery passed only after actual invocation. Choose browsers by live capability and platform login state. First use of each platform uses login/work tabs in one Profile.

[Browser selection / 浏览器选择](../operations/browser-selection.md) · [Bridge / 桥接恢复](../operations/browser-recovery.md) · [Receipts / 回执](../operations/onboarding.md)
