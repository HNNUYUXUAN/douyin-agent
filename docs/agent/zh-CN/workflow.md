# 理解作品与交付

[English](../en/workflow.md) · [索引](../index.json)

## 适用意图

对已经取得的单条或批量作品完成用量预览、理解、证据复核和文字交付；也用于复用已完成结果。

## 前置条件

工作区和运行环境已配置；新处理所需的实际素材与取得回执可用。收费处理必须先通过完整性检查，受有效用量授权约束。

## 最少输入

用户的理解问题、实际 JOB 目录或批次 jobs 清单；执行时使用本次预览产生的 PLAN 和 ID。完成任务的后续文字问题只需定位其已有结果。

## 操作步骤

先读取本地 `agent-context.json`（若存在），以真实安装路径确定 Python、技能和工作区；必要时走 [首次使用](onboarding.md)。用户可直接提供链接、分享文案、本地素材，或要求宿主在抖音检索主题。站内搜索由连接浏览器完成，CLI 不提供抖音关键词搜索。

以下命令统一使用 `PYTHON SKILL/scripts/da.py --workspace WORKSPACE COMMAND`。`JOB` 是实际返回的任务目录，`PLAN` 与 `ID` 来自当前预览；不要复制旧任务的值。

`ID` 是当前预览 JSON 的 `id` 字段；`PLAN` 是本次自动保存的计划文件绝对路径 `WORKSPACE/out/plans/ID.json`（将 WORKSPACE 和 ID 替换为实际值）。预览打印 JSON，不单独返回路径；先确认该文件存在，再把它传给 `--plan`。

1. 开始任务运行 `cleanup --expired`。查看 `status`；已有相同作品 ID/媒体哈希任务优先复用。完成的文字结果直接读取，新增画面问题重新获取。
2. 浏览器打开目标作品，核对 ID、作者、标题、完整文案、源时长或图文数量与顺序。获取遵循 [取得协议](../../../references/browser.md)：先复用已成功的免费解析来源，再尝试实际可用的宿主下载能力，每轮最多三个不同来源。只提交公开链接，不交账号凭据。
3. 下载后检查真实首尾画面。视频回执使用 `source_id`、`identity_verified`、`page_duration`、`head_tail_verified`、`method`、`host`；图文记录 `expected_images` 与 `order_verified`。仅新下载副本可列入 `owned_downloads`，每项有绝对 `path`、`sha256` 和 `created_by_task:true`。本地用户原件不登记为可删除副本。逐张图片下载受阻时，按 [ZIP 批量取得](acquisition.md#图文逐张下载受阻zip-批量获取) 使用 `unpack_images.py --archive ABS --workspace ABS --output NEW_ABS_DIR --expected-images N`，输出目录必须是工作区内不存在的 ASCII 子目录；宿主逐张核对原页后才确认顺序。ZIP 不传给 adopt；把有所有权证据的临时 ZIP 和解包图片列入回执 `owned_artifacts`，字段为绝对 `path`、`sha256`、`created_by_task:true`。命令及完整回执示例见该取得指南。
4. `adopt "SOURCE" --media "FILE1" "FILE2" --receipt "RECEIPT.json" --title "TITLE" --author "AUTHOR" --caption "CAPTION"` 返回 JOB 和完整性结果。单个视频每项一个文件；图文按原顺序提供多个文件。本地视频也需首尾复核；本地图文也需数量和顺序回执。源时长未知、身份不符、截断或解码失败时停止该项云调用。`integrity --job JOB` 可重查。
5. `preview --jobs JOB1 JOB2 --question "QUESTION"` 生成用量预览；或 `--manifest FILE` 读取含 `jobs` 数组的批次 JSON。展示时长、图片数、分段覆盖、模型、缓存和新增调用上限。默认随时长自适应采样；音频完整覆盖，视觉不是逐帧观看。重要片段可写 JOB 下 `extra-frames.json` 时间秒数数组再预览。
6. 取得本预览授权，或确认有效持续授权覆盖后，运行 `run --plan PLAN --approve ID`。扩展素材或范围必须重新预览；下游摘要按最坏请求数预留，缓存命中不重复收费。
7. `run` 返回 `review_ready` 后，宿主逐项抽查关键数字、公式、代码、字幕冲突、图文顺序；修订 `analysis.md` 并写 `review.json`，记录 `status:sampled/verified`、当前 `analysis_sha256`、非空 `checks`（证据编号/时间与实际观察）。不查看原帧就不能声称已复核。
8. `finalize --job JOB` 先校验文字，再清理已登记的任务媒体，包括 owned_artifacts 中的临时 ZIP 和解包图片；JSON manifest 与回执作为文字审计保留。只有两者成功才是 `completed`；`cleanup_pending` 进入 [恢复](recovery.md)。最后 `validate --job JOB`，交付报告和结果目录链接。

长期结果使用 MD/JSON：原生字幕时序、语音文字、逐段观察、证据编号/哈希、报告、校验和清理记录。原生时间缺失时保留文本并明确限制，不编造时间戳。报告不嵌本地图片或失效媒体链接。保留用户原件、环境和私密配置。

公开视频受限不等于批次全部失败；记录该项原因并继续其他独立作品。服务认证、额度和未决请求问题按恢复指南处理，不通过新任务 ID 绕过。

## 预期输出与成功依据

先到 review_ready，复核后 finalize 完成文字校验与登记媒体清理，最终状态为 completed。交付 analysis.md 与证据 JSON，并以 validation/cleanup 结果核对成功范围。

## 停止或恢复条件

完整性失败、计划变化、未决请求、认证/额度错误、缺复核或清理失败时，不宣称完成；按 [恢复指南](recovery.md) 处理，扩大输入或用量需新预览。

## 下一步链接

继续读取完成报告；新画面问题回到 [取得作品](acquisition.md)，异常进入 [恢复指南](recovery.md)。


v2.4：终端按已有 Git Bash → PowerShell 7 → Windows PowerShell 5.1 选择，记录实际路径/版本。WorkBuddy 新安装使用用户级 `.workbuddy/skills/douyin-agent`，已有安装沿用回执；会话目录和运行工作区分开。时间戳以系统 UTC 为准。新增平台/视觉/浏览流程从 [会话指南](browse.md) 按需加载。下载和检索为两层：免费解析站优先；寻找来源用已有检索技能 → 宿主搜索 → 已配置元宝/博查。缺少检索能力时打开服务官方入口，让用户本地配置 Key。`parsed_download_failed` 表示解析成功但文件未落地，所有来源尝试均计入每轮三源上限。用户协助提供本地文件后保留原件，重新核对身份、首尾、时长或图片顺序。不要读取未知剪贴板来寻找下载地址。
