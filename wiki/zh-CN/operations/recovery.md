---
{
  "type": "Runbook",
  "title": "请求恢复、清理与迁移",
  "description": "请求恢复、清理与迁移",
  "tags": [
    "douyin-agent",
    "zh-CN",
    "recovery",
    "v251-runtime"
  ],
  "status": "active",
  "generated": {
    "by": "douyin-agent/2.5.1",
    "at": "2026-11-05T15:01:35.569439+00:00"
  },
  "sources": [
    {
      "resource": "https://requests.readthedocs.io/en/latest/user/quickstart/#timeouts"
    },
    {
      "resource": "../../shared/acceptance/runfix-v251.md"
    }
  ],
  "applicability": {
    "skill": "2.5.1 candidate",
    "host": "Capability-detected; local and recipient evidence separate"
  },
  "verification_scope": "Implementation and offline fixtures; live scope is listed in acceptance evidence."
}
---

# 请求恢复、清理与迁移

触发：读取超时、SSE 中断、截断、未决占用或恢复停止。适用 v2.5.1 候选；先确认实际工作区、原 plan/job/cache_id 和运行锁，保留原记录。

所有命令前缀为 `PYTHON SKILL/scripts/da.py --workspace WORKSPACE`；使用回执里的真实绝对路径。只读排查：
```text
requests status
requests status --cache-id CACHE_ID
requests reconcile --cache-id CACHE_ID
requests retry --cache-id CACHE_ID
requests retry --cache-id CACHE_ID --approve RECOVERY_PREVIEW_ID
resume --plan WORKSPACE/out/plans/ORIGINAL_PLAN.json --approve ORIGINAL_PLAN_ID
requests abandon --cache-id CACHE_ID
```
`status` 只读展示提交、尝试链、缓存和有效阻塞。其他 requests 操作有工作区锁；只允许一个流水线进程，沿用进程句柄等待，不能反复开 shell 或截图轮询。每 15 秒的本地进度 JSON 与最终结果分开读取。

`reconcile` 核验已保存完整成功结果，或 `--evidence WORKSPACE_RELATIVE.json` 的可靠关联证据。必须匹配已知平台响应 ID、completed 和完整文本；本地 cache_id 是内容缓存身份，不能当平台请求 ID。不猜测平台查询接口；默认 store:false。已完整写入缓存但账本未更新时也能核对。没有可靠证据返回未知，不修改原占用。

`retry` 先生成额外用量预览，再用其 id 授权；有效会话授权覆盖新增用量即可继续，开发验收沿用维护授权。每个逻辑请求最多一次未决续跑，产生关联原记录的独立 attempt 和独立占用。授权后 resume 原计划，从失败步骤继续，复用成功 ASR、视觉与下载。原 unknown/pending 和原 charge 始终保留。第二次仍未决只能核对或结束；不能删 pending、改旧预算、换作品绕过。

`abandon` 保存失败摘要、恢复记录和 abandoned 状态，并清理路径、哈希及所有权核验通过的任务媒体；无需伪造成功报告。用户导入原件、未知文件、账本和未知终态保留。单个作品未决只阻塞其有效尝试链；独立作品继续。认证、额度和模型配置错误暂停相关云调用，修正后走明确恢复入口。

连接默认 30 秒、无数据读取默认 300 秒，可在本地 .env 设置 `VOLC_AGENT_CONNECT_TIMEOUT` / `VOLC_AGENT_READ_TIMEOUT`（1～1800 秒）。这是连接／空闲读取限制，并非整个请求总时限。超时不改内容缓存身份。视觉／汇总／报告输出上限为 4096／4096／8192，写入预览和缓存身份；截断不成为成功缓存。

诊断覆盖提交、响应头、首事件、首文本和完成，记录实际模型、请求／响应 ID、usage、错误阶段及耗时；缺失字段保持未知。没有响应头或响应文件不能证明服务端未处理。ASR 保持完整音频、协议节奏，分别记录上传与识别等待，不推测上传加速协议。

成功判据：原计划到 review_ready，宿主对照真实帧／音频复核并写匹配报告哈希的 review，再 finalize。完成后可直接复用文字。失败媒体仍有原 24 小时到期清理；主动结束可提前清理；二者都不释放请求占用。迁移仍先 dry-run，再无活跃进程时 apply，保留原件和账本。
