---
{
  "type": "Runbook",
  "title": "跨浏览器选择与双标签协作",
  "description": "跨浏览器选择与双标签协作 — douyin-agent operational knowledge",
  "tags": [
    "chrome",
    "edge",
    "login",
    "登录",
    "双标签",
    "browser"
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

# 跨浏览器选择与双标签协作

## 实时探测

使用宿主实际提供的浏览器清单和标签清单，覆盖已连接的 Chrome、Edge 及可见实例。先看所选平台的现有标签；必要时在候选实例打开该平台公开页验证。只检查选定平台，记录连接、DOM、截图和文件保存四项能力。不要扫描浏览器用户数据、Cookie 或未连接 Profile。

根据当前可见登录按钮、账号入口及页面状态判断 `logged_in|logged_out|unknown`；同时记录页面访问 `passed|blocked|unverified`。头像或可播放本身不能单独证明已登录。登录态是当时的观察。

## 选择和复用

用户指定实例优先；否则实时核验上次绑定，再从能访问目标作品的已登录实例中选择。只有一个候选则采用；多个等价候选让用户选一次并记录绑定。没有已登录实例时，可复用能读公开页的实例；提供公开链接仍能进入解析站。

新 `onboard --record` v2 回执记录不含账号名的浏览器 ID、类型、四项能力、各平台登录/访问状态和平台标签绑定。返回的 `browser_choices` 是历史建议，操作前必须重新核对。连接 ID 变化后重新观察；不要照抄旧标签 ID。

## 首次两个标签

首次使用选定平台时，在同一实例、同一 Profile 创建或复用登录标签 A 和工作标签 B。A 留给用户登录、验证码或确认已有登录态；B 用于浏览和取得公开链接。保持两个标签分工，不在用户登录期间导航 A。

实际完成引导后保存 `first_use_complete`、`browser_id`、`login_tab`、`work_tab` 和证据。后续实时复核后复用工作标签。仅关闭 Agent 为探测创建且不再需要的标签；用户原有标签及登录页保留。

WorkBuddy 5.9.3 / 扩展 0.2.8 异机回传证明了扩展登录态可复用，并记录了内置实例的登录态问题；这不是所有内置浏览器版本的统一结论。运行时按实际能力选择。


[桥接与截图恢复 / Bridge recovery](browser-recovery.md) · [v2 receipt example](../../../docs/agent/examples/onboard-v2.json)


## Login handoff / 登录交接

用户需要登录接管时，使用宿主实际提供的保留／交接能力保留登录标签；等待期间不导航或关闭该标签。
