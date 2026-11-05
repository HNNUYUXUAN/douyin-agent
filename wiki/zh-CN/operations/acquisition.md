---
{
  "type": "Runbook",
  "title": "通过解析站取得媒体",
  "description": "通过解析站取得媒体 — douyin-agent operational knowledge",
  "tags": [
    "parser",
    "download",
    "解析站",
    "下载",
    "user_import"
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

# 通过解析站取得媒体

## 开始前

先核对目标作品身份、可靠时长或图片总数和原顺序；再验证宿主能把文件保存到本机并返回确切路径。页面可读、按钮存在与解析成功分别记录。无法保存文件时记 `host_download_unavailable`，提供用户本地文件导入入口，其他独立作品继续。

## 来源发现与尝试

读取 `providers`，优先复用在当前宿主和平台上验证有效的免费解析站。失效或不足时，使用已有检索插件／skills → 宿主原生搜索 → 已配置元宝、博查。都不可用时提供安装或官方服务配置引导，让用户本地填写 Key。搜索结果是候选，需现场验证免费、适用平台和实际保存能力。

平台账号用于正常浏览、核对和取得公开链接。媒体统一交给解析站；已有下载工具只负责保存解析结果。只提交公开作品链接。解析站要求账号、Cookie、付费或额外插件时记录受阻；保留用户提供原件。

每个作品的本轮使用稳定 `round_id`，访问解析站前先写 `outcome=attempting`。每轮最多三个不同来源；登录墙、验证码、不可达和文件取得失败均计数。失败不自动建新轮。来源回执的 `url`、`search_source` 用无凭据、无查询串的公开 HTTPS 入口；同一来源完成后更新原 `round_id` 的结果。

## 回执和文件核验

新 `adopt` 回执必须包含 `route=parser|user_import`。解析路线同时填写 `provider`、`host`、`round_id`，关联已经记录的来源尝试；`provider` 是解析站入口。`user_import` 保留用户原件，不登记原件为 `owned_downloads`。

视频核对作品、音视频轨、全解码、可靠时长和首尾；图文核对全部图片、数量与原顺序。图文解析结果可以是站点提供的 ZIP，按 ZIP 指南安全解包后逐张核对。获取成功必须以文件落地及完整性通过为依据，再把 provider 更新为 `success` 并关联实际 `job`。

`parsed_download_failed` 表示解析成功但文件保存失败；`login_required`、`captcha_required`、`quota_exhausted`、`unavailable` 和 `failed` 分别记录。不要读取未知剪贴板寻找地址。签名下载地址仅用于当次传输，不写入长期来源记录。

任务新下载文件以绝对路径、SHA256、`created_by_task:true` 登记。已登记媒体及辅助截图在复核后清理；保留 MD/JSON、回执、用量、恢复记录和用户导入原件。旧回执继续用于历史任务恢复。


[任务命令 / Task commands](workflow.md) · [ZIP images](zip-images.md)

[文件保存探测与同轮标准传输恢复](../operations/parser-sites.md)。已有 curl 可以保存解析站公开文件链接；浏览器下载接口缺失时分别探测。
