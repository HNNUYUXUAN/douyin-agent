---
{
  "type": "Runbook",
  "title": "恢复、清理与历史迁移",
  "description": "恢复、清理与历史迁移 — douyin-agent operational knowledge",
  "tags": [
    "douyin-agent",
    "zh-CN",
    "operations",
    "recovery"
  ],
  "status": "active",
  "generated": {
    "by": "douyin-agent/2.5.0",
    "at": "2026-11-05T02:27:48.555869+00:00"
  },
  "sources": [
    {
      "resource": "https://github.com/GoogleCloudPlatform/knowledge-catalog/blob/62432a095456147ee71e70ac6e4dc0d2dea3ac30/okf/SPEC.md"
    }
  ],
  "applicability": {
    "skill": "2.5.x",
    "host": "capability-detected; see body for measured versions"
  },
  "verification_scope": "Documentation reviewed; runtime acceptance is recorded separately."
}
---

# 恢复、清理与历史迁移

[English](../../en/operations/recovery.md) · [索引](../../../docs/agent/index.json)

## 适用意图

诊断并处理环境/取得/请求/复核/清理失败，读取清理后的文字结果，或迁移历史任务。

## 前置条件

可以只读访问实际工作区和任务记录；先保留现有状态。未决请求不得用重试或修改账本解除，活跃进程保护规则继续有效。

## 最少输入

目标 job 或计划标识、具体症状；请求问题需要原 plan/job/cache_id 及可获得的平台证据，缺失字段保持未知。

## 操作步骤

先运行只读 `status`、`doctor` 或 `onboard --check`，确认问题属于环境、浏览器、取得媒体、服务请求、复核还是清理。详细约束见 [恢复协议](../../shared/recovery-protocol.md)。

| 状态/症状 | 下一步 |
|---|---|
| 浏览器断连/切换配置 | 按首次引导重新发现并绑定标签页，核对账号和访问权限；不重新提交已在途的任务 |
| 取得受限/完整性未知 | 记录原因，停止此项收费理解；可请求本地素材，其他独立作品继续 |
| `review_ready` | 核对原帧并写匹配当前报告哈希的复核记录，然后 finalize |
| `cleanup_pending` | 检查具体路径、哈希、取得证据与文件占用，修复后重试 finalize；不扩大删除范围 |
| 已完成且媒体已清理 | 读取文字结果；新画面问题重新取得素材并预览 |
| 未决付费请求 | 保留原账本及预算占用，优先核对原请求；不能直接重发 |

### 未决请求：先只读取证

本版本**没有 `reconcile` 命令**。对于尚未完成的 job，`run/resume` 发现该 job 的任意 pending 记录就停止，不自动跳过，也不自动重提；这可能中止当前批次。`resume` 不是超时后的通用重试按钮。

以下命令使用 `PYTHON SKILL/scripts/da.py --workspace WORKSPACE COMMAND`。排查只运行 `status`（需要时加 `doctor` 或 `onboard --check`），不要用 `run/resume` 或 `cleanup` 代替只读诊断。

1. 从 `status` 的 `jobs` 找到目标任务绝对路径及 `state.status`，从 `pending` 取得待核对的文件名；同时记下 `locked`。读取目标 job 的 `metadata.json`，核对 `source.id`、`media_identity`，确保排查的是原作品。
2. 读取相关 `cache/<cache_id>.pending.json`，收集 `cache_id`、`job`、`plan`、`at`、`status`、`error_type`（若有）、`charge`，以及 `identity.stage`、模型及处理版本字段（若有）。`job` 可能是任务目录名或 `out/jobs/...` 相对路径，须与目标绝对路径对应。不要只按最新时间推测归属。
3. 在 `requests.json` 数组中以 **plan + job + cache_id** 对照同一提交，保留所有匹配记录；记录 `status`、`charge.audio_seconds/images/requests`、`request_id`、`usage`、`billing` 和 `error_type`（存在时）。请求 ID 缺失就记未知，不能编造。再读 `out/plans/<plan>.json` 的 `id`、目标 `jobs`、`new_usage`、模型及选项，对照原批准范围，不修改计划 ID 或预算。
4. 若存在 `cache/<cache_id>.response.json`，只读核查它属于该原请求的证据。记录 `id`/`log_id`、`status`、`incomplete_details.reason`、`error`、`usage`（存在时）。传输中断记录可能是 `{status:transport_interrupted,response:...,partial_text:...}`；外层中断状态和内层响应状态要分别记录，`partial_text` 不是完整结果。没有响应文件不等于没有发生计费。
5. 如有平台可查的原请求 ID，核对平台原请求的终态和完整结果。将上述标识、证据来源、查询时间及仍未知的字段写入单独的工作区 MD/JSON 取证记录，供维护者协助；不要把 Key、Cookie、认证头、完整私人响应或签名媒体地址发到聊天或公开 issue。

**没有可核实的原请求终态及完整成功结果时，保留原占用并停止这个 job。** `incomplete/length` 虽是已知截断终态，仍不是完整成功结果。不得拼凑部分输出为成功缓存，不得删除 pending、改写账本状态/预算或新建同作品 job 来解锁。即使拿到平台证据，本版本也没有自动导入/核销接口；维护者协助应单独记录原请求与平台证据，不按这份指南手工改运行状态。

可以为其他独立作品形成独立预览，在有效授权范围内继续；不要把受阻 job 混入这批。只有确认目标 job 没有 pending、现有输入及元数据仍与原计划一致、用量和授权范围未扩大时，才执行 `resume --plan PLAN --approve ID`。它复用已有完整缓存并继续尚未完成的步骤；仍可能发生预览内的新调用。扩大范围则重新预览，不能修改旧计划来通过检查。

已经完成并清理媒体的任务直接读取其 `analysis.md`、`understanding.json`、`segments.json` 等文字结果，可用 `validate --job JOB` 校验；不要为了读总结重新提交原请求。新的画面问题需要重新取得素材并预览。服务 `usage` 保留原值，与平台结算账单分别标注。

失败/中断任务自首次失败起暂留媒体 24 小时，查看或恢复不续期。`cleanup --expired` 只在任务入口或宿主明确调用时执行，没有后台定时器。活跃或无法确认的进程锁保护媒体。先核对锁的 PID 和创建标识，不能为方便运行直接删锁。

历史升级先 `migrate --dry-run` 检查路径、请求数、音频秒数、图片数和未决记录，再在没有活跃 worker 时 `migrate --apply`。代码和文字备份放技能发现目录外；用户原件保留，媒体不备份、不能回滚。每项文字验证后才清理，迁移前后账本与未决哈希必须一致。

清理只允许所有权记录中的逐文件删除。工作区外下载副本必须核对绝对路径、取得记录和 SHA256；未知文件保留并报告，禁止清空下载目录或浏览器缓存。清理不会解除未决请求保护。

## 预期输出与成功依据

只读调查形成可追溯的原因、证据和下一步，未决占用保持。只有下文恢复条件满足才继续任务；清理后读取以已有报告和校验为依据，未知情况不会被标成成功。

## 停止或恢复条件

找不到可核实终态/完整结果、存在 pending 或活跃/未知锁、所有权不明时，停止依赖该条件的恢复动作；按下文详细步骤保留证据交维护者协助。

## 下一步链接

满足条件后回 [任务流程](workflow.md)；需重新取得画面时读 [取得作品](acquisition.md)，实现层协助见 [维护指南](maintenance.md)。
