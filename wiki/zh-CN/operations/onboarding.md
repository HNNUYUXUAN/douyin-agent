---
{
  "type": "Runbook",
  "title": "首次配置检查与当前观察回执",
  "description": "首次配置检查与当前观察回执",
  "tags": [
    "onboard",
    "setup",
    "record",
    "skill_discovery",
    "observed",
    "key"
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

# 首次配置检查与当前观察回执


## 固定入口
首次完整读取 [必读包](../bootstrap/first-run.md)。普通 setup 只配置；use 等用户开工；acceptance 仅维护验收。Key 缺失必须停下等本地填写，配置完成不自动运行作品。
## 命令
使用实际安装器返回的路径：
`PYTHON SKILL/scripts/da.py --workspace WORKSPACE onboard --check --flow setup --host workbuddy --language zh-CN --observed CURRENT_JSON`
不带 --observed 时，返回本地检查和历史建议，要求宿主补本次观察；不能据旧 passed 宣称完成。--browser-id OPAQUE_ID 固定用户指定实例；不可用就恢复连接。Codex 使用 --host codex。
输出：一个 next_action、required_docs、blocking_reasons、waiting_for、phase 和 setup_status。next_actions 为兼容保留的单元素列表。必读路径相对于技能根。按当前步骤执行后复查，不把这些宿主动作当本地脚本自动执行。
## 只读与保存
--check／--observed 只读、不打开页面、不调用服务；--record CURRENT_JSON 保存 onboarding.json、agent-context.json 和最小 setup-progress.json。record 不应与 observed 同时使用。恢复用 phase、证据和 next_action，重新核对实时条件。进度不保存 Key、页面正文或账号。
## 回执
仍接受 v1（schema_version、checks）和 v2（再增加 browser_observations、platform_bindings）。检查项每项仅 status、observed_at、evidence；status 为 passed|blocked|unverified|not_applicable。skill_discovery 新增为宿主实际发现，列表证据与新聊天调用范围分别写在引用证据中。全部 observed_at 读取实际系统钟；evidence 使用已有工作区相对 MD/JSON，或无查询串的公开 HTTPS。完整验收模板不能直接传入；只提取有真实时间的 checks，browser_bridge 映射 browser_connection，安装／清理项保留在验收表。
v2 的浏览器四项 capabilities 仍为 connection/dom/screenshot/file_save。新增可选 host_capabilities，为宿主实际返回能力名列表；WorkBuddy 平台选择必须含 user_tabs，旧回执缺失时重新观察。family=chrome|edge|other，kind=extension|iab|cdp；只有 Chrome/Edge 用户扩展可用于平台。
CURRENT_JSON 必须是本次重新观察，不能仅复制旧文件／更新其时间戳。脚本验证格式和来源，不证明宿主真的执行过动作。
## 结果与停止
依赖、安装回执、技能发现、用户浏览器 DOM／截图和本地 Key 满足后返回 finish_setup；云字段仍为 false，报告“本地配置已完成，真实服务尚未验证”。没有收费测试。平台文件保存／登录按后续开工范围探测。
依赖缺失按返回手册补齐；浏览器失效按恢复分支；Key 缺失必须等待。填写后复查一次，仍缺则继续等待，不自动跳过。
## 示例
[v2 回执](../../../docs/agent/examples/onboard-v2.json) 仅为格式示例，必须替换成实际观察。登录标签按 [浏览器判定](browser-selection.md) 条件创建，不能照抄示例 passed。
