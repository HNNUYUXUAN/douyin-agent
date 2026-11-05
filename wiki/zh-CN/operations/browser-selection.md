---
{
  "type": "Runbook",
  "title": "用户浏览器选择与条件登录标签",
  "description": "用户浏览器选择与条件登录标签",
  "tags": [
    "browser",
    "chrome",
    "edge",
    "user_tabs",
    "login",
    "双标签"
  ],
  "status": "stable",
  "generated": {
    "by": "douyin-agent/2.5.1",
    "at": "2026-11-05T09:57:06.630627+00:00"
  },
  "sources": [
    {
      "resource": "https://www.codebuddy.cn/docs/workbuddy/From-Beginner-to-Expert-Guide/Function-Description/Right-Sidebar"
    }
  ],
  "applicability": {
    "skill": "2.5.1 candidate",
    "host": "Windows x64; recheck current host capabilities"
  },
  "verification_scope": "Candidate implementation; fixture, local and recipient results are recorded separately."
}
---

# 用户浏览器选择与条件登录标签


## 触发与适用
本技能所有平台页面，包括公开页面、短链核对和登录页。适用 Chrome／Edge 用户扩展连接；内置浏览器仅处理公开解析站／说明。
## 前置检查
列出实际连接实例，记录 family、kind、连接、DOM、截图及文件保存。WorkBuddy 还必须观察 user_tabs，写入 host_capabilities；旧回执未记录则要求实时补查，不推断缺插件。不读取 Cookie、凭据、浏览器用户数据或未连接 Profile。
## 执行顺序
1. 用户指定实例：只选择该实例。失效返回 connect_user_browser，读恢复手册；不静默切换。
   连接／DOM 正常但平台页面受限时返回 platform_blocked，保留指定实例，按页面／登录分支处理，不重装健康桥接。
2. 未指定：实时复核历史绑定；否则选择能访问目标的已登录实例。多个等价实例选一次并记录。内置实例永不进入平台候选。
3. 无所选平台的观察时先 probe_platform，不能把浏览器连接或头像单独当登录成功。记录 login_state=logged_in|logged_out|unknown 与 access 独立；证据冲突时保留 unknown 再核对账号控件。
4. logged_in：只复用／创建工作标签，login_action=not_needed。logged_out／unknown：同 Profile 创建或复用登录标签和工作标签，login_action=reserve_login_tab；将登录标签交给用户，不导航、不关闭。已给公开链接可走解析站，无需等待登录才能解析。
5. 登录确认后，只关闭本任务新建、已完成交接且不再需要的登录标签；用户原有标签保留。先记录标签所有权；选择器返回的待释放 ID 不构成删除授权。
6. 后续复查后复用工作标签。内置解析站跳转回平台时，在所选用户浏览器核对，不能沿用内置页面做平台观察。
## 成功判据与上限
页面访问、登录、播放、截图、文件保存分别核验。一次选定后复用；失效先完整读取 [恢复](browser-recovery.md)，不能靠反复换浏览器试错。
## 记录和恢复
`onboard --check --host workbuddy --browser-id OPAQUE_ID --observed CURRENT_JSON` 使用本次观察；`--record` 保存 v1／v2 回执。结果依然是建议，实际导航由宿主执行；本地脚本不能拦截宿主绕过流程的网页动作。
