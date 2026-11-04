---
{
  "type": "Runbook",
  "title": "未决请求恢复",
  "description": "先读实时 status 和原计划，按 job 与 cache_id 查账本和 pending；保留占用，不自动重提。",
  "tags": [
    "timeout",
    "pending",
    "超时",
    "额度",
    "quota",
    "authentication"
  ],
  "status": "draft",
  "generated": {
    "by": "douyin-agent/2.3.0",
    "at": "2026-11-04T10:31:25.341864+00:00"
  },
  "sources": [
    {
      "resource": "https://github.com/HNNUYUXUAN/douyin-agent/blob/main/docs/agent/zh-CN/recovery.md"
    }
  ]
}
---

# 未决请求恢复

先读实时 status 和原计划，按 job 与 cache_id 查账本和 pending；保留占用，不自动重提。

[执行指南 / Execution guide](https://github.com/HNNUYUXUAN/douyin-agent/blob/main/docs/agent/zh-CN/recovery.md).

[其他问题 / Other topics](index.md).
