# Lifecycle / 生命周期与恢复

`run/resume` consumes an approved immutable plan and enters review_ready. Review key digits, code/formulas, captions, timeline and image order against actual frames. Correct analysis.md where necessary, then write review.json with status sampled/verified, analysis_sha256 and checked evidence observations. `finalize --job` validates durable text before deletion and is idempotent. Missing/unregistered files or deletion failures cannot be called completed. Fix file locks/ownership records with evidence, then repeat finalize.

`run/resume` 使用当前批准计划，完成后为 review_ready。宿主复核并修订报告，review.json 必须匹配当前 analysis.md 哈希，附抽查时间/图号与观察。finalize 校验文字后清理；失败为 cleanup_pending。不得为删除方便将用户文件改为任务所有。

Failed/interrupted media expire 24 hours after first failure; repeat status/resume does not renew expiry. Every new adopt/preview/run/resume starts cleanup --expired. Doctor/status do not mutate or contact services. Workspace lock uses PID and process creation token; active/unknown locks prohibit cleanup. Provably dead locks are archived as JSON and orphan processing tasks become interrupted. No background scheduler. After cleanup, cached text remains readable; new visual work requires reacquisition and preview.

失败/中断的媒体保留24小时，不因查看/恢复续期。任务入口清理，doctor/status只读。PID加创建时间防止PID重用误判；活跃或无法确定的进程保护媒体。无后台任务。清理后文字照常读取，新的画面问题重新获取。

Each paid call reserves requests.json and a cache pending record before sending. No automatic retry. Transport failure stays unresolved and charged. Authentication/quota/service errors stop cloud calls. This version has no `reconcile` command or automatic result-import interface. An unfinished job with any matching pending record is blocked by run/resume, even if other calls for that job have cached output. Do not delete pending files, rewrite ledger state/budgets, assemble partial outputs into successful caches or create a new job for the same work to bypass protection.

付费请求先占用 requests.json 与 pending，再提交；超时不自动重试。当前版本没有 reconcile 命令或自动结果导入接口。未完成 job 存在任何匹配 pending 时，run/resume 停止；部分步骤有缓存不能解除该保护。不得删 pending、改账本状态/预算、拼接部分结果冒充完整缓存，或新建同作品任务绕过。

Read-only investigation starts with status. Match the target metadata/source and each requests.json submission against cache/<cache_id>.pending.json using plan + job + cache_id; retain all matching records. Collect timestamps, status, error_type, stage/model/version, charge, request_id/log_id, usage and billing where present. Read the original out/plans/<plan>.json to establish scope. For cache/<cache_id>.response.json, distinguish the outer transport_interrupted wrapper from any nested response; collect terminal status, incomplete_details.reason and errors. Missing fields remain unknown, and missing response files do not prove zero charge. See the step-by-step [English guide](../docs/agent/en/recovery.md) or [中文指南](../docs/agent/zh-CN/recovery.md).

只读排查先 status，按 plan + job + cache_id 对照原作品、requests.json、pending 及 response.json，保留全部匹配提交。收集时间、状态、错误类型、阶段/模型/版本、提交量、请求标识、usage 和 billing；回看原计划范围。response.json 的外层传输中断与内层响应状态分开记录，缺失字段保持未知，不能据无响应文件判定零计费。具体字段和步骤见上面的双语指南。

Without verified terminal-state evidence and a complete successful original result, preserve reservations and stop that job. Server-confirmed incomplete/length is terminal but unsuccessful; partial output is never complete evidence. When platform lookup is available, retain its evidence and the original request in a separate investigation record for maintainer assistance. Evidence collection does not automatically unlock the job, and these guides provide no manual ledger/pending-edit procedure. Other independent works may proceed in a separate authorized preview. Only resume a target with no pending records, unchanged plan inputs/metadata and unexpanded authorization. Already completed/cleaned text is read directly; cleanup never changes request reservations. Returned usage is separate from settled billing.

未能核实原请求终态及完整成功结果时，保留占用并停止该 job。服务器明确 incomplete/length 仍是未成功的截断结果，不拼凑缓存。可查询平台时，另存原请求及平台证据交由维护者协助；取证不会自动解锁，本指南不提供账本/pending 手工修改步骤。其他独立作品可单独预览继续。仅目标无 pending、原计划输入和元数据未变、授权未扩大时才 resume。已完成且清理后的文字直接读取；清理不改请求占用。usage 与结算账单分别标注。

## Migration / 迁移

Run `migrate --dry-run`, inspect totals/paths, then `migrate --apply`. No live worker is allowed. Back up code and text outside the skill discovery directory. Imported originals are excluded. Native subtitle JSON and human edits remain; legacy SRT/TXT are preserved as JSON text records. Each legacy job must validate before media removal. JSONL submissions become atomic JSON with unchanged records, charges and pending hashes. Media are deliberately excluded from backups and cannot be rolled back. External copies require separate exact acquisition/hash evidence.

先 dry-run 核对，再 apply；必须没有活跃worker。先保存代码/文字备份，迁移原生字幕与人工修订，通过验证才删除受管媒体；账本逐条及未决哈希前后一致。已清理媒体不备份。外部下载必须另外核对取得记录和哈希，其他项目原件保留。

Installation uses delivery.json allowlist and receipts containing SHA256. Compare the previous release hashes before replacing files, preserve user changes and .env, and save rollback code outside skill discovery. Source/runtime/private config are exempt from text-only result retention. Rollback restores code, not deleted media.

Historical maintainer-assisted recovery may be documented in acceptance evidence; it is not a public automatic recovery command. The internal reuse_cache_ids field only reuses complete existing caches and does not resolve pending requests. Do not hand-edit a preview to use that field. Historical authorized resubmissions retain original request charges and do not establish that an incomplete response can be marked successful.

验收记录可能包含历史维护者协助恢复，它不代表当前公开 CLI 有自动恢复命令。内部 reuse_cache_ids 只复用完整缓存，不处理未决请求；不要为使用该字段手工改预览。历史授权重提保留原计费占用，不能据此把截断响应标成成功。
