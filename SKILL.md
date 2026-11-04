---
name: douyin-agent
description: 使用火山 Agent Plan 理解多平台视频、图文、分享链接与本地媒体，生成可追溯的文字报告并清理任务媒体。Use for bounded multi-platform browsing and evidence-based video/image-post understanding with text-only retention.
---
# douyin-agent

仅安装 WorkBuddy 与连接器的新设备，先读 [中文从零引导](references/bootstrap/zh-CN/first-run.md) / [English zero-start](references/bootstrap/en/first-run.md)。遇到新问题先检索 [OKF Wiki](wiki/index.md)，依语言 [记录与检索](references/bootstrap/zh-CN/knowledge.md) / [knowledge operations](references/bootstrap/en/knowledge.md) 保存脱敏本地经验。

按用户语言读取 [中文执行参考](references/zh-CN/workflow.md) 或 [English execution reference](references/en/workflow.md)，再按意图加载其中链接的详细指南。Read only the reference and guides relevant to the current task.

用户提供主题、作品链接、分享文案、本地素材或批次时，由宿主检索、核对作品并取得媒体。本地脚本检查完整性、预览调用、执行处理；Agent Plan 转写与分析。使用实际采样画面和原生语音时间，宿主复核后保存 MD/JSON 并清理已登记的任务媒体。视觉是采样，无法完整取得或核实的作品须报告限制。

使用本机 `agent-context.json` 中的实际技能、工作区与 Python 路径，恢复时重新读取实时状态与账本。首次安装读 [AGENT_INSTALL.md](AGENT_INSTALL.md)；首次配置或能力失效按所选语言参考中的引导执行。Key 由用户在本地填写，进程环境变量优先；本地检查不等于浏览器或云服务验证。

遵循取得与完整性检查 → 预览及授权 → 执行 → `review_ready` 原帧复核 → `finalize` → `completed`。新增素材或扩大范围重新预览；已有持续授权在范围内有效。收费请求不自动重试，未决请求保留预算并停止该任务重提。仅清理经所有权、路径和哈希核对的任务媒体，保留用户原件。详见 [取得协议](references/browser.md) 和 [恢复协议](references/recovery.md)。

命令入口：`PYTHON SKILL/scripts/da.py --workspace WORKSPACE COMMAND`；替换为实际绝对路径，含空格加引号。`doctor`、`status`、`onboard --check` 只读。分发使用 `delivery.json`，排除凭据、环境、缓存及私人媒体；验证范围见 [验收记录](references/acceptance.md)。

用户明确开工后，先按语言读取 [受控浏览](docs/agent/zh-CN/browse.md) / [finite browsing](docs/agent/en/browse.md)。平台、模式和额度由用户选择，无默认消费模式。需要看图时加载视觉指南并使用已配置 Agent Plan；按会话预算持续执行，失败项留待处理，其他独立作品继续。
