---
{
  "type": "Runbook",
  "title": "哔哩哔哩：视频、分 P 与图文动态",
  "description": "哔哩哔哩：视频、分 P 与图文动态 — douyin-agent operational knowledge",
  "tags": [
    "bilibili",
    "哔哩哔哩",
    "BV",
    "分P",
    "dynamic",
    "图文"
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

# 哔哩哔哩：视频、分 P 与图文动态

## 来源与身份

支持 `www.bilibili.com/video/BV…/?p=N`、av 视频分享、`b23.tv`、`t.bilibili.com/动态ID` 和 `www.bilibili.com/opus/动态ID`。av、短链先由宿主在可见页面解析到 BV 或动态。视频身份是 `bilibili:BV…-pN`；省略 p 使用 p1。不同分 P 分别核对标题、时长和会话额度；全部分 P 需要用户范围覆盖。动态身份使用 `bilibili:dynamic-ID`。

## 页面与控件

实时读取可见 DOM 和语义按钮，核对标题、UP 主、当前分 P、时长或图片总数。播放、静音、进度、自动连播与下一 P 均以当前页面重新定位；没有本机新版本定位证据时保持未验证。首次点击播放后等待数秒，再检查进度；占位图不能证明插件拦截。每次只有一条任务视频播放，正常速度、静音、不拖动；记录实际经过时间、结束状态与可能的循环。

图文按原图顺序逐张打开并按会话停留规则观察，区分预览缩略图、正文图片与转发原文。转发动态分别保存转发文案和原作品链接／可见内容；纯文字动态只记录页面观察。视频动态转到所关联 BV，保留动态到视频的关联证据。

## 媒体取得与恢复

把公开链接交给免费解析站，按获取指南登记来源、下载结果和文件完整性。图文须核对全部图片与顺序；分 P 须确认解析结果就是指定 P。解析站只返回封面、首 P 或部分图片时不得标记完整。无法取得时记待处理并提供用户导入。

登录墙、412、验证码、删除、付费或直播分别记受限。回传曾验证过的匿名接口取流属于历史证据；本版本不执行接口取流。已有登录态用于正常浏览和页面核对，不用于媒体提取。

## 验证范围

异机回传：Windows Server 2022、WorkBuddy 5.9.3、扩展 0.2.8，BV1dC4y117Rz 作品页面及 1080P 起播通过；媒体曾经由匿名接口取得。这不证明本版解析站、分 P、动态链路通过。本版实测结果见发布验收记录。


[Acquisition / 获取](../operations/acquisition.md) · [Browsers / 浏览器](../operations/browser-selection.md)


## Local controls / 本机控件

本轮 Chrome 156：语义按钮“播放/暂停”“音量”；音量数字 0 为实际静音依据，即使 video.muted 为 false。P2 页面显示（2/3）、P2、00:22，下载文件 21.12 秒。图文正文 `.b-img__inner img` 当次为 1 张，正文“6 个地区”不是图片数。以上定位每次重新观察；完整播放与页面观察分别记录。
