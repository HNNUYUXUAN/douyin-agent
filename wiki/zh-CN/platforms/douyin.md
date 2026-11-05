---
{
  "type": "Runbook",
  "title": "douyin 操作指南",
  "description": "douyin 操作指南 — douyin-agent operational knowledge",
  "tags": [
    "douyin-agent",
    "zh-CN",
    "platforms",
    "douyin"
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

# douyin 操作指南

## 验证范围
v2.4 实际控件与链路范围见下方记录；TikTok 本轮只提供待实测流程。历史抖音 Codex 案例和 WorkBuddy 5.9.3 的页面读取证据不替代本版本端到端验收。

## 操作
1. 用宿主当前可用的浏览器打开用户指定推荐页、搜索页或作品页；确认实际 URL、作者、作品 ID、标题、时长/图片数。登录、验证码交用户处理。
2. 从实时 DOM 的 role、name、label 或 title 找搜索输入框、播放/暂停、静音、进度、下一条、图片前后切换。记录候选控件的语义与状态；不要猜测工具名。
3. 点击静音后核对静音状态；播放后读取实际进度，正常速度等待结束，确认结束状态再前进。缺语义加载 [视觉指南](../operations/vision.md)。
4. 图文核对当前图片序号和总数，逐张前进，保留原顺序。完整性未知时不送云深析。
5. 免费解析来源优先，寻找来源按已有检索技能 → 宿主搜索 → 元宝/博查。文件落地后核对完整性；失败写 deferred，不声称下载成功。

## 记录与恢复
控件摸排记录宿主、浏览器/扩展版本、页面类型、观察时间、定位依据、动作前后状态与脱敏证据。公共指南只收经审阅的通用语义；账号和浏览内容留本地。控件失效重新观察，视觉失败保留待办并继续独立作品。


## 本次控件观察

2026-11-04 Windows Codex Chrome：作品页实际出现 `xg-icon.xgplayer-play`、`xg-icon.xgplayer-volume`；点击音量后 video.muted=true，播放/暂停有效。可读 video.duration/currentTime/playbackRate。此样本87.034秒；只摸排控件，未将该条标为完整播放。
