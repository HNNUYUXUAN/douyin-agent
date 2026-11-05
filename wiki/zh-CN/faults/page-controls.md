---
{
  "type": "Runbook",
  "title": "页面初始化、输入与滚动恢复",
  "description": "页面初始化、输入与滚动恢复",
  "tags": [
    "page-controls",
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

# 页面初始化、输入与滚动恢复

触发：空 DOM／临时“出错啦”、输入 applied:true 但值为空、cua_scroll 超时或滚动后空白。适用回传 WorkBuddy 5.9.3／扩展 0.2.8 的观察；其他版本现场核对。实际根因可能是焦点、首屏或宿主通道，不能仅凭现象断定框架缺陷。
前置：记录浏览器／标签 ID、实际失败接口和页面状态。确定是用户 Chrome／Edge；不在用户正在登录的标签上试验。
执行：
1. 首屏空白：等待 3–10 秒后重读 DOM／标题，最多两次检查；有明确 412／登录墙时记录对应限制，不能用瞬时标题替代结论。
2. 输入后回读 input value 并比对目标链接；不一致时重新观察、点击真实输入框、确认焦点后 Ctrl+A，重输一次。提交前再次回读；仍不一致就停止本站尝试。工具 applied:true 不证明页面接受输入，不读未知剪贴板。
3. 滚动接口超时：停止重复该接口；用一次 PageDown／PageUp 或可见锚点，再观察 DOM。必要时先保存当前输入与进度，再重载工作页一次恢复渲染。保留用户标签和登录交接。
4. 播放器占位：按平台指南点击播放、等待初始化，检查本任务其他播放器和自动连播；不自动关闭用户在播标签。不据占位推断广告插件故障。
成功：实际 DOM／输入值／视图位置／播放进度分别符合目标；截图与播放结束分开记录。
上限：输入纠正一次、首屏两次检查、替代滚动一次、工作页重载一次；无新证据不重复。
停止／恢复：静态桥接健康时不重铺运行时；持续失败保存状态，转 [未知故障](unknown.md)。
