---
{
  "type": "Runbook",
  "title": "Agent Plan 本地 Key 配置",
  "description": "Agent Plan 本地 Key 配置",
  "tags": [
    "key",
    "setup",
    "waiting",
    "local_key"
  ],
  "status": "stable",
  "generated": {
    "by": "douyin-agent/2.5.1",
    "at": "2026-11-05T09:44:27.533063+00:00"
  },
  "sources": [
    {
      "resource": "https://www.volcengine.com/activity/agentplan"
    }
  ],
  "applicability": {
    "skill": "2.5.1 candidate",
    "host": "Windows x64; recheck current host capabilities"
  },
  "verification_scope": "Candidate implementation; fixture, local and recipient results are recorded separately."
}
---

# Agent Plan 本地 Key 配置


## 触发与适用
首次配置完成依赖、安装和浏览器连接后；适用 Windows 宿主。已有有效 Key 直接复用，不重复购买或填写。
## 前置检查
只读 doctor／onboard 的 key_present；进程环境优先于工作区 .env。Key 存在不证明套餐或真实请求通过。
## 执行
缺失时打开 [官方入口](https://www.volcengine.com/activity/agentplan) 和 [控制台](https://ark.volcengine.com/region:cn-beijing/openManagement?LLM=%7B%7D&advancedActiveKey=agentPlan)，展示本次实际 WORKSPACE/.env 路径。用户自行登录、购买并填写 VOLC_AGENT_API_KEY；不要在聊天索取、回显、截图或读取整个环境变量表。
运行 `onboard --record CURRENT_JSON` 保存当前非敏感观察和等待位置；当前阶段为 key 时 waiting_for=local_key。明确等待用户填写并结束当前执行，不继续下载、浏览会话或收费调用，没有跳过选项。
## 核验与上限
用户确认填写后进行一次本地检查；仍缺失就继续等待。已有进程环境覆盖空白 .env 时以实际读取优先级为准，不显示值。该步骤不调用 API。
## 完成与恢复
全部必要项满足后 finish_setup，报告本地配置已完成、真实服务尚未验证。恢复时复用安装结果；真实任务等用户另行开工。专属 Plan Key 与其他产品 Key 不混用。
