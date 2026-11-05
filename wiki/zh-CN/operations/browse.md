---
{
  "type": "Runbook",
  "title": "有限浏览与会话授权",
  "description": "有限浏览与会话授权 — douyin-agent operational knowledge",
  "tags": [
    "douyin-agent",
    "zh-CN",
    "operations",
    "browse"
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


# 有限浏览与会话授权

## 适用与前置条件
用户明确开工后执行。浏览器、文件、终端能力已核对；按需加载 [平台指南](platforms.md)、[视觉辅助](vision.md) 和 [取得流程](acquisition.md)。技能不安装常驻进程或定时任务。

## 开工选择
一次询问尚缺字段：平台、入口/主题、模式、精选规则、时长/条数、图文停留、云用量。模式为 browse（浏览记录）、selective（精选深析）、all（逐条深析），三者平级，没有默认选择。用户已明确的字段直接采用。仅选择浏览仍可能用到视觉辅助；宿主 token 不能读取时显示 unknown。

配置示例是格式样本，不是消费授权。请用本次用户选择替换每个值：
```json
{"platforms":["douyin"],"mode":"browse","entry":"current recommendations","selection":"","max_seconds":600,"max_items":3,"image_dwell_seconds":3,"limits":{"requests":0,"images":0,"audio_seconds":0,"search_requests":0}}
```
max_seconds/max_items 至少一个为正数；未采用的一个显式写 null。零云额度表示仅走已有 DOM 等不新增技能云调用的路线。

## 命令与执行
命令前缀为 `PYTHON SKILL/scripts/da.py --workspace WORKSPACE`，路径取本机实际值。
```text
browse create --config CONFIG_JSON
browse approve --session SID --approve APPROVAL_ID
browse status --session SID
browse record --session SID --file OBSERVATION_JSON
browse pause --session SID
browse resume --session SID --approve APPROVAL_ID
preview --jobs JOB --session SID --question QUESTION
search --session SID --query QUERY
```
create 只保存待授权会话并返回 SID/approval_id；向用户展示实际配置后，在有效授权覆盖下 approve。resume 同样需要用户明确发起。所有浏览器动作由宿主实际执行，脚本记录观察与限制，pause 之后宿主也应暂停播放器。

每次打开作品先核对平台/ID、身份和时长，读取 `browse status`。已知时长大于剩余会话时间则不开始。静音、正常速度、从头单次播放，不拖动进度、不循环刷同一作品。等待使用宿主已提供的等待机制，分段等待并检查结束；保留用户中止机会，避免每秒截图和模型调用。图文逐张按原顺序浏览，遵循选定停留时间。

观察 JSON 至少含 source、status（played/observed/deferred）。可附 title、observation、reason；精选项记录 selected:true 与 selection_basis。played 需要 playback 对象：muted:true、rate:1、seeked:false、duration、start、end、elapsed_seconds（秒），以实际观察填写；图文记录 images、images_visited。脚本检查证据结构，不自行测量浏览器。页面观察或完整播放不能替代完整媒体理解。

需要深析的作品经取得及完整性检查后，先 record，再生成带 --session 的具体 preview；在本次会话规则和剩余额度内 run，无需逐条重新确认。超过预算保存待办，不扩大范围。鉴权/额度/未决问题暂停有关云调用，保留占用；其他可独立完成的 DOM 浏览继续。下载失败、控件失效、视觉失败写 deferred 和准确原因，结束时集中反馈。未决请求不自动重提。

## 产物与恢复
工作区 out/sessions/SID/session.json 保存选择、观察、状态，usage 从账本实时计算。作品仍走 review_ready → 真实原帧复核 → finalize → completed。保留 MD/JSON，任务媒体和截图按所有权、路径、哈希清理，用户原件保留。停止和恢复只读实时状态，不以历史记录推断成功。


## 播放和平台阻塞

先关闭本任务自动连播，再静音、正常速度顺序播放。占位图或 00:00 时点击并等待数秒，检查同站在播标签后再排查网络或可见拦截证据；用户原有标签不自动关闭。当前页无法取得作品 ID 时，可 `browse record` 写平台入口 source、status=deferred、reason；结果存 pending，不占作品条数、不授权深析。新授权 ID 绑定会话和配置；旧会话继续读取。

[Recovery / 恢复](browser-recovery.md)


平台枚举：douyin、youtube、xiaohongshu、tiktok、bilibili。
