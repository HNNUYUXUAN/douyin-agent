# 首次使用与配置恢复

[English](../en/onboarding.md) · [索引](../index.json)

## 适用意图

首次使用技能，或恢复失效/变更的浏览器和 Agent Plan 配置。

## 前置条件

已有安装及可定位的工作区；宿主能够引导用户完成浏览器连接。登录、购买和本地 Key 填写仍由用户完成。

## 最少输入

实际 Python/技能/工作区路径、用户选择的浏览器，以及待记录的实际观察。真实服务验证另需具体样例和覆盖用量的授权。

## 操作步骤

安装前分别检查终端、Conda 基础解释器、工作区 Python 3.12 和 FFmpeg；终端可用不代表运行环境已准备。详见 [安装指南](install.md)。

目标是让用户集中完成必要的连接、登录、购买和本地 Key 填写，此后复用有效配置。宿主执行检查与打开页面；安装脚本不能证明浏览器已连接。已有有效项目直接复用，不反复要求用户配置。

### 先检查，再引导

运行 `PYTHON SKILL/scripts/da.py --workspace WORKSPACE onboard --check`。这是只读检查，不创建记录、不打开浏览器、不发起云调用。读取实际报告中的下一步；`doctor` 检查本地环境，`status` 查看任务，均不证明套餐可用。

由宿主分别核验：浏览器连接、选定配置、抖音页面可访问、必要登录状态、Agent Plan Key 本地存在、真实服务样例是否已验证。不得把其中一项成功推断为其他项成功。使用 `onboard --record FILE` 保存非敏感宿主检查；记录写入工作区 `onboarding.json`，并更新本地 `agent-context.json`。两者只供后续路由，不包含凭据或私人页面内容。

### 浏览器

WorkBuddy 使用自己的 [宿主连接指南](../../../references/bootstrap/zh-CN/workbuddy.md)，浏览器连接按其设置与工具核验；下述 Codex UI 说明仅适用于 Codex。


本机优先已连接 Chrome；用户选择 Edge 时使用该浏览器自己的配置和权限。根据 [官方连接说明](https://learn.chatgpt.com/docs/chrome-extension)，引导用户在桌面宿主 Settings → Computer Use 安装/管理对应扩展，并在聊天选择 `@Chrome` 或 `@Edge`。入口随宿主版本变化时以实际 UI 为准。

连接成功后，在同一浏览器配置中打开 [抖音](https://www.douyin.com/)。用户按需登录、处理验证码和权限提示。宿主实际读到页面标题或目标作品后才记录访问通过。不能要求用户导出 Cookie。浏览器未连接时先提供官方说明链接，让用户完成连接，再自动打开余下页面；不要声称已打开无法访问的标签页。

### Agent Plan

集中打开缺失步骤对应的官方页面：

| 页面 | 用户操作 |
|---|---|
| [购买页](https://www.volcengine.com/activity/agentplan) | 自行登录并选购套餐；已有套餐直接复用 |
| [Agent Plan 控制台](https://ark.volcengine.com/region:cn-beijing/openManagement?LLM=%7B%7D&advancedActiveKey=agentPlan) | 获取 Agent Plan 专属 Key，查看实际套餐权益 |
| [官方快速开始](https://docs.volcengine.com/docs/ark/agent-plan-personal-get-started?lang=zh) | 核对产品配置说明 |

宿主创建并打开工作区 `.env`，用户自行填 `VOLC_AGENT_API_KEY`。不要索取聊天中的 Key，不截图或回显凭据。保留已有文件；进程环境变量优先于工作区 `.env`。专属 Key 与普通方舟/Coding Plan Key 不通用；固定 Plan 端点已由脚本设置，用户无需改 Codex 的主模型配置。

购买、付款、登录和验证码由用户完成。价格、额度和套餐权益以当时控制台为准；不要将历史 Small 套餐实测等同于所有账号当前可用。不会自动开启续费或超额付费。

### 验证与复用

Key 存在后先做本地检查。真实服务测试使用一个具体、已取得的作品，按 [任务流程](workflow.md) 先展示用量预览，再在用户授权范围内运行。失败按实际 HTTP/协议证据记录；未知保持未知。保存完成状态和仍需处理的步骤。后续只复查失效、变更或缺失部分；切换浏览器配置后重新核验该配置。

### 宿主检查回执

以下仅为格式示例，替换为实际观察；不得将示例 passed 状态作为测试证据。`status` 允许 `passed`、`blocked`、`unverified`、`not_applicable`；`observed_at` 使用实际 UTC 时间；`evidence` 是可核对的公开 URL 或工作区相对 JSON 证据路径。只记录 `browser_connection`、`douyin_access`、`agent_plan_call`，不保存账号或浏览器配置名称。

```json
{
  "schema_version": 1,
  "checks": {
    "browser_connection": {
      "status": "passed",
      "observed_at": "2026-11-03T00:00:00Z",
      "evidence": "https://www.douyin.com/"
    },
    "douyin_access": {
      "status": "unverified",
      "observed_at": "2026-11-03T00:00:00Z",
      "evidence": "qa/onboarding-check.json"
    },
    "agent_plan_call": {
      "status": "unverified",
      "observed_at": "2026-11-03T00:00:00Z",
      "evidence": "qa/onboarding-check.json"
    }
  }
}
```

`onboard --record FILE` 记录宿主观察；随后 `onboard --check` 返回本地检查及历史观察，不把历史 passed 等同于当前权限或服务可用。

## 预期输出与成功依据

只读检查给出本地状态与历史观察；记录操作生成非敏感 onboarding.json 和 agent-context.json。每个通过项有实际观察，缺项保持待处理；不将历史记录当实时可用性证明。

## 停止或恢复条件

连接、登录、验证或 Key 填写未完成时，只暂停依赖该条件的动作；本地检查可继续。真实请求异常按 [恢复指南](recovery.md) 保留原占用。

## 下一步链接

配置就绪后读 [取得作品](acquisition.md)；已有素材则进入 [任务流程](workflow.md)。
