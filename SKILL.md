---
name: douyin-agent
description: 使用火山 Agent Plan 自适应理解抖音视频、长视频、图文、分享文案和本地媒体；完整性检查、分段证据、MD/JSON交付并清理临时媒体。Use for Douyin video/image understanding with verified acquisition, adaptive segments and text-only retention.
---
# douyin-agent v2.1.0

按用户语言从 [Agent 操作索引](docs/agent/index.json) 选择当前任务；常用入口为 [中文任务流程](docs/agent/zh-CN/workflow.md) / [English workflow](docs/agent/en/workflow.md)。从仓库安装先读 [AGENT_INSTALL.md](AGENT_INSTALL.md)，首次使用或配置失效读 [中文首次引导](docs/agent/zh-CN/onboarding.md) / [English onboarding](docs/agent/en/onboarding.md)。

复用本地 agent-context.json 中的实际路径与已记录状态；onboard --check 只读检查，浏览器和真实服务仍需宿主分别核验。工作区建议 D:\douyin-agent；不存在 D 盘时选择其他可写短路径。复用已有 Conda，缺失时给官方安装指引。Key 只在本地 .env 填写，不进入聊天。进程环境变量优先。

宿主需要浏览器、搜索、文件和媒体处理能力；本机优先连接 Chrome。开始任务先 cleanup --expired；doctor/status 只读，不验证服务额度。浏览器获取遵循 [获取协议](references/browser.md)，当前主机的成功来源优先，blob/失败时检索免费解析服务，每轮最多三个来源。只提交公开作品链接。永不将网页摘要或片段当完整分析。

核对作品 → 获取并登记所有权 → integrity → preview → 用户批准当前计划 → run/resume → review_ready → 核对关键原帧 → 写 review.json → finalize → completed。新增素材或扩大调用范围必须重新预览；已有持续用量授权在其范围内有效，不重复询问。

默认 auto 采样；音频覆盖全片，视觉为分布式采样，不保证看到每一帧。代码/公式/字幕冲突用 extra-frames.json 补帧并重新预览。先逐分钟理解，再分层总结。ASR 时间只能来自服务器，不推算字幕。外部事实核查属于可选扩展，详见 references 中的流程；与作品内容分开，不作为首次使用前置条件。

run 后必须审核关键数字、公式、图文顺序及证据编号。review.json 记录抽查项、时间/图号、观察、修订与 analysis_sha256。finalize 先验证文字，再逐文件清理登记媒体；两者成功才 completed。只保留 MD/JSON；用户导入原件保留。没有媒体时复用文字，新的画面问题重新获取。

付费调用不自动重试。未决请求占用预算，清理媒体不解除保护。失败保留24小时，按首次失败计算；不安装后台任务。具体恢复、迁移、清理见 [recovery](references/recovery.md)。升级前检查发布哈希，代码/文字备份放技能发现目录之外，保留环境和私密配置。

运行命令 PYTHON SKILL/scripts/da.py --workspace WORKSPACE COMMAND（PYTHON 使用 setup 返回的解释器，SKILL 替换为已安装技能的绝对目录）。完整命令和回执例子见语言流程。分发是普通目录，使用 delivery.json 白名单，禁止打包凭据、环境、缓存或私人媒体。验证状态以 [acceptance](references/acceptance.md) 为准，不将本机测试描述为异机成功。
