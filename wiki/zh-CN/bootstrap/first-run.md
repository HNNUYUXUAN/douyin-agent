---
{
  "type": "Runbook",
  "title": "首次配置：固定步骤与停止条件",
  "description": "首次配置：固定步骤与停止条件",
  "tags": [
    "setup",
    "首次安装",
    "first-run",
    "gate"
  ],
  "status": "stable",
  "generated": {
    "by": "douyin-agent/2.5.1",
    "at": "2026-11-05T09:57:06.630627+00:00"
  },
  "sources": [
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

# 首次配置：固定步骤与停止条件


## 执行前完整阅读

只选当前语言。按顺序完整读取本页、[依赖](dependencies.md)、当前宿主 [WorkBuddy](workbuddy.md) 或 [Codex](codex.md)、[浏览器](../operations/browser-selection.md)、[Key](key.md)、[故障索引](../faults/index.md)。本次已读且内容未变时复用，不重复加载。机器清单见 docs/agent/index.json 的 setup_flow。

## S0 判断意图

普通安装／配置使用 setup；日常任务使用 use；只有用户明确要求维护验收才用 acceptance。普通安装不运行升级、中断、重复安装、全套测试、多平台作品或收费样例。

## S1 只读自检

从实际源码根运行 `scripts/preflight.ps1 -Workspace ABS_WORKSPACE -TargetHost workbuddy`（Codex 改为 codex）。Windows 自带 PowerShell 即可，不要求 Python；常规安装仍使用返回的 Git Bash → PowerShell 7 → 5.1。输出实际路径、版本、缺失依赖、安装回执和必读包。可写性标 unverified；首次真实写入由安装器检查。

## S2 补缺和安装

按 [依赖](dependencies.md) 补缺，再读 [安装步骤](../operations/install.md)，调用现有 install.sh／install.ps1。已有回执及配置先复用；安装成功不重复安装来“确认”。失败先读命中手册，保留环境和回执。

## S3 宿主发现与连接

记录技能实际发现；同一聊天与新聊天分别声明，不能自行新开聊天则保留该项待验收，不重装。按宿主指南核对 Chrome／Edge 扩展、DOM 与公开页面截图。只检查本次必要实例；不遍历五个平台。没有选平台时，不创建平台登录标签。

## S4 Key 等待

缺 Key 时按 [Key 手册](key.md) 输出本地路径与官方入口，保存等待状态并结束当前执行，等待用户填写。没有跳过入口，不继续作品下载、浏览会话或模型调用。

## S5 配置收尾

使用安装器返回的 Python 和技能根：`PYTHON SKILL/scripts/da.py --workspace WORKSPACE onboard --check --flow setup --host workbuddy --observed CURRENT_JSON`。CURRENT_JSON 是本次实际观察，格式见 [回执](../operations/onboarding.md)。返回一个 next_action；完成当前步骤后再检查。`--record CURRENT_JSON` 才保存观察和 setup-progress.json。

finish_setup 时报告“本地配置已完成，真实服务尚未验证”，并结束。真实作品等待用户明确开工；不因持续额度授权自动创建样例。

## 恢复与停止

恢复先看 setup-progress.json、实际回执和当前缺项；重新取得实时宿主观察，不复制旧 passed。故障读对应完整手册，核验后记录；未知故障按 [交接](../faults/unknown.md)。分别记录依赖下载、安装、用户等待、故障及维护验收耗时；宿主积分和 Agent Plan 用量分列，未知不估算。


预检明确调用方式：在实际源码根用 `powershell.exe -NoProfile -File ./scripts/preflight.ps1 -Workspace ABS_WORKSPACE -TargetHost workbuddy`。将 ABS_WORKSPACE 替换为本设备短路径并引用含空格参数；不要把 .ps1 当 Git Bash 脚本直接执行。预检返回必读包供首次完整阅读，后续 onboard 只返回当前阶段文档，已读内容复用。
