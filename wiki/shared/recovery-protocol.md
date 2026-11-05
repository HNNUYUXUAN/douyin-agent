---
{
  "type": "Runbook",
  "title": "Lifecycle / 生命周期与恢复",
  "description": "Lifecycle / 生命周期与恢复 — douyin-agent operational knowledge",
  "tags": [
    "douyin-agent",
    "shared",
    "recovery-protocol"
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

# Lifecycle / 生命周期

Read the complete language-specific [English recovery manual](../en/operations/recovery.md) or [中文恢复手册](../zh-CN/operations/recovery.md).

提交先保留占用；明确核对、一次独立续跑与主动结束均通过 requests 命令执行。原账本及未知终态保留。Complete caches are reused; partial or truncated responses are never successful evidence. Review precedes successful finalization; explicit abandonment can clean verified owned media without a successful report. Preserve user imports and unknown files.
