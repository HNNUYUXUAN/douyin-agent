---
{
  "type": "Runbook",
  "title": "浏览器、截图与下载回执",
  "description": "浏览器、截图与下载回执",
  "tags": [
    "douyin-agent",
    "zh-CN",
    "runtime-host",
    "v251-runtime"
  ],
  "status": "active",
  "generated": {
    "by": "douyin-agent/2.5.1",
    "at": "2026-11-05T15:06:20.335700+00:00"
  },
  "sources": [
    {
      "resource": "https://requests.readthedocs.io/en/latest/user/quickstart/#timeouts"
    },
    {
      "resource": "../../shared/acceptance/runfix-v251.md"
    }
  ],
  "applicability": {
    "skill": "2.5.1 candidate",
    "host": "Capability-detected; local and recipient evidence separate"
  },
  "verification_scope": "Implementation and offline fixtures; live scope is listed in acceptance evidence."
}
---

# 浏览器、截图与下载回执

触发：找不到浏览器、扩展未连接、截图超时、导出未知、节点失效或点击下载无产物。适用 v2.5.1 候选。先读取宿主实例和页面证据，不读取 Cookie、凭据、Chrome Preferences 或私人临时目录。

1. 用户指定 Chrome／Edge 时平台及解析站均沿用该实例；未指定时按浏览器选择手册。浏览器进程未启动、扩展未连接、标签未授权、页面失败分别记录。Windows 可运行 `powershell.exe -NoProfile -File SKILL/scripts/browser-ready.ps1 -Browser Chrome -Mode Check`；安装范围内 `-Mode Launch` 启动已选浏览器后，只作少量宿主连接检查。此脚本不证明扩展连接，不停止用户浏览器。连接健康不重装桥接。
2. 桥接只读检查兼容真实终端：Git Bash 中 `powershell.exe -NoProfile -File 'C:/skill/scripts/workbuddy-bridge.ps1' -Mode Check -Browser Chrome,Edge`；PS7 中 `& 'C:\skill\scripts\workbuddy-bridge.ps1' -Mode Check -Browser @('Chrome','Edge')`。替换实际技能路径；严格只接受 Chrome／Edge。
3. 已登录直接工作标签；未登录或未知时同 Profile 保留登录标签与工作标签。等待期间不操作登录标签；公开链接可直接进解析站。页面可读与可播放分开记录。
4. 截图先确认并聚焦目标标签。内联截图成功和导出成文件分别核对；不能导出就记录能力限制，使用 DOM 或明确的文件入口，不搜索私人缓存。超时按截图手册诊断一次，不循环重装健康桥接。
5. 优先语义控件。只有 node_id 时，页面变化后重新观察；stale 后只重新定位一次。输入后回读真实 value，提交前再核对。初始化空 DOM 先等待并有限复查。滚动通道失败改键盘导航，再观察。
6. 点击下载前：`PYTHON SKILL/scripts/save_watch.py --workspace WORKSPACE before`，保存 watch_id。点击后 `... after --id WATCH_ID`。无文件为 not_observed，多文件为 ambiguous；这不证明整个宿主无法下载。仅经宿主确认本任务创建的确切文件，才加 `--expected-name FILE --confirm-created-by-task`。不根据最近时间认领用户文件。回执给出路径、大小、SHA256；仍须解码、身份、时长／图序核对。

成功：正确实例连接及当前 DOM／截图能力分别有证据，取得必须有实际文件完整性回执。上限：连接和聚焦后有限复查、stale 一次；同链接明确拒绝不重复切代理。保存错误、实例、阶段、恢复位置后交接。缺 Key 保持本地填写等待，普通安装到配置完成即收尾。
