---
{
  "type": "Runbook",
  "title": "媒体身份、采样与清理故障",
  "description": "媒体身份、采样与清理故障",
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

# 媒体身份、采样与清理故障

触发：尾帧无输出、清理路径不匹配、分 P／图序不一致、截图受策略限制。适用已取得的任务媒体；不改变解析站路线。
前置：核对实际取得回执、哈希、所有权、原文件及原始时间轴，不以浏览器播放完成代替文件完整性。
执行：视频按有效视频流时间采尾帧，缺尾帧只能在完整解码通过后记录降级；中间解码故障准确报错，不剪短原文件假装通过。B 站按 BV+分P、动态独立身份；av／短链通过用户浏览器页面确认。图数按作品原图，拼图分区不是独立图片。
Windows 路径表示可统一，哈希、所有权及重定向保护必须保留；cleanup_pending 先查确切错误，不删整个任务／缓存目录。用户导入原件保留，未知下载不动。图文 ZIP 保留原件，提取副本按清单核对。
截图能力分别核对。宿主截图失败先走截图分支；系统 Add-Type 被策略阻止时不改安全策略。确有必要且宿主允许时，只用已有 FFmpeg 采任务公开区域并登记所有权，不能采凭据页面。
成功：完整性与身份通过、原帧／原图复核有证据、只清理可核对的任务媒体；MD/JSON 和未决账本保留。
上限：按实际修复原因复验一次，不为新报告重跑已完成收费分析；空 ASR 不代表静音。
停止／恢复：读取 [任务流程](../operations/workflow.md) 和 [恢复](../operations/recovery.md)，受阻保存清理／解码错误交接。
