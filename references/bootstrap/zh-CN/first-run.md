# 从零开始

适用：Windows x64 新设备仅安装 WorkBuddy 与 Chrome/Edge 连接器。标准技能入口文件名是 `SKILL.md`（大写单数），旁边的 scripts 和 references 随安装保留。

1. [获取源码和依赖](dependencies.md)：无需预先安装 Git、Python 或 Conda；宿主先检查实际终端，使用 Windows 自带 PowerShell 下载源码。
2. [WorkBuddy 宿主配置](workbuddy.md)：核对当前用户目录，把技能安装到其 `.codebuddy/skills/douyin-agent`；验证客户端发现和实际浏览器连接。
3. [首次配置](../../../docs/agent/zh-CN/onboarding.md)：宿主打开抖音、Agent Plan 购买页、控制台及本地 .env，用户完成登录/购买/Key 输入。
4. [首条任务](../../../docs/agent/zh-CN/workflow.md)：给实际作品链接，核对与取得媒体，完整性通过后展示预览；在有效授权内执行，复核并 finalize。
5. [排错与知识积累](knowledge.md)：先检索文档和私有案例，按证据处理，保存脱敏问题记录。
6. [全新设备验收](clean-test.md)：逐项记录结果；缺项写 blocked，不从本机历史记录推断通过。

用户第一条消息可复制：

```text
请从 https://github.com/HNNUYUXUAN/douyin-agent 安装 douyin-agent。
先读 AGENTS.md、AGENT_INSTALL.md 和 references/bootstrap/zh-CN/first-run.md。
这是只安装 WorkBuddy 和浏览器连接器的新 Windows 设备。请探测并准备源码、Conda Python 3.12、媒体工具和 WorkBuddy 技能目录，逐步完成首次配置。
需要登录、购买、填写 Key 或系统授权时打开对应页面并让我完成。然后展示实际小样本用量预览，再在授权范围内验证。
遇到问题先查 Wiki，记录可复用的脱敏事实与未解决项。
```
