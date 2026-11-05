---
{
  "type": "Runbook",
  "title": "首次接入与恢复",
  "description": "首次接入与恢复 — douyin-agent operational knowledge",
  "tags": [
    "douyin-agent",
    "zh-CN",
    "bootstrap",
    "first-run"
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

# 首次接入与恢复

按以下顺序逐项核对；已有配置直接复用，只补缺失或失效的部分。每项分别记 passed / blocked / unverified。

1. 探测现有 Git Bash → PowerShell 7 → Windows PowerShell 5.1，记录实际可执行文件和版本；检测架构、磁盘、可写短工作区和宿主会话目录。
2. 取得同一发布提交的普通源码目录，复用 Conda、Python 3.12、FFmpeg/FFprobe；缺失按依赖指南准备。
3. WorkBuddy 新安装使用当前用户 `.workbuddy/skills/douyin-agent`，已有安装沿用回执。实际调用技能后记录发现结果。
4. 探测已有检索技能、宿主原生搜索以及文件保存能力。下载工具用于保存解析站结果。
5. 用户选择本次平台后，再枚举所有已连接 Chrome/Edge，检查该平台可见标签和登录状态，完成首次双标签引导。其他平台按首次使用分别接入。
6. 复用已配置 Agent Plan；缺配置时打开官方入口，让用户在本地填写 Key。首次配置不自动发起收费任务。
7. 用户明确开工并确定模式与范围后，用具体样本预览，在既有授权范围内执行、复核、清理和记录。

登录、验证码、购买和凭据输入交给用户。平台未登录仍可处理公开链接并访问解析站。历史通过记录需重新核对当前能力。


[依赖 / Dependencies](dependencies.md) · [WorkBuddy](workbuddy.md) · [浏览器 / Browsers](../operations/browser-selection.md) · [配置回执 / Receipts](../operations/onboarding.md) · [浏览 / Browse](../operations/browse.md)

[文件保存探测与同轮标准传输恢复](../operations/parser-sites.md)。已有 curl 可以保存解析站公开文件链接；浏览器下载接口缺失时分别探测。
