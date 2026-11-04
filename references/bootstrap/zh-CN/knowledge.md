# 知识检索与记录

公开 [wiki/index.md](../../../wiki/index.md) 是按 Google OKF 0.2 组织的知识包，包含安装、宿主和恢复概念；[固定规范](https://github.com/GoogleCloudPlatform/knowledge-catalog/blob/62432a095456147ee71e70ac6e4dc0d2dea3ac30/okf/SPEC.md)。每个概念是 Markdown + YAML frontmatter，路径为身份；索引和日志使用 index.md、log.md。脚本写入 JSON 映射形式的合法 YAML，因此不新增 YAML 库。

公开 Wiki 随版本只读分发；私有案例写到工作区 `knowledge-private/`。搜索/validate 只读，init/reindex/record 写文件。检索只是关键词匹配，不依赖向量数据库、额外 Key 或 Google 云账号。协议不保证宿主自动识别 Wiki，SKILL.md 与 Agent 索引显式提供入口。

```text
PYTHON SKILL/scripts/knowledge.py --workspace WORKSPACE search --query "WorkBuddy browser 连接"
PYTHON SKILL/scripts/knowledge.py --workspace WORKSPACE init
PYTHON SKILL/scripts/knowledge.py --workspace WORKSPACE record --file CASE_JSON
PYTHON SKILL/scripts/knowledge.py --workspace WORKSPACE validate
```

先检索公开概念和本地案例，再读实时 status、相关指南与实际错误。结果带 public/private 和文档路径；案例中的历史结果不证明当前环境可用。修复后复验，将现象、采取的动作、实际结果、验证证据、关键词写成 JSON；格式见 [脱敏示例](../../../docs/agent/examples/case.json)。sources 仅用干净公开 HTTPS URL 或已存在的工作区相对 MD/JSON 证据。不要把 Key、Cookie、签名地址、机器绝对路径、私人转写、账号资料或原媒体填入案例。脚本拒绝常见凭据/路径模式，提交前仍由宿主检查脱敏。

record 要求新 ASCII id，已有案例不可覆盖；修订用新 id 并在动作中提及旧案例。保存状态始终 draft，不自动宣称已由人复核。中断后用 reindex 重建索引与日志；原问题事实和未决账本仍以工作区证据为准。私有案例不会自动上传或进入分发；需要公开的经验须单独脱敏审阅。
