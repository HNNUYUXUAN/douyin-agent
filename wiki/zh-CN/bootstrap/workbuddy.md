---
{
  "type": "Runbook",
  "title": "WorkBuddy 宿主接入",
  "description": "WorkBuddy 宿主接入 — douyin-agent operational knowledge",
  "tags": [
    "douyin-agent",
    "zh-CN",
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

# WorkBuddy 宿主接入

新安装使用当前用户 `.workbuddy/skills/douyin-agent`，已有安装沿用安装回执。运行工作区与宿主会话目录分开记录。实际调用技能后才记录发现通过。浏览器按实时连接能力、平台登录状态选择；首次每个平台采用同一 Profile 的登录／工作双标签。

[Browser selection / 浏览器选择](../operations/browser-selection.md) · [Bridge / 桥接恢复](../operations/browser-recovery.md) · [Receipts / 回执](../operations/onboarding.md)
