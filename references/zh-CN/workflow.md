# 中文执行流程

使用 setup.ps1 返回的 Python3.12 解释器。以下 P 表示该解释器，S 为技能目录，W 为工作区；路径含空格须用引号。命令入口：`P S/scripts/da.py --workspace W COMMAND`。

1. `doctor` 检查本地配置存在性与媒体工具；`status` 只读查看状态。开始工作用 `cleanup --expired`。首次配置见 README。
2. 按获取协议由宿主核对作品并取得媒体。公开视频回执包含 source_id、identity_verified、page_duration、head_tail_verified、method、host；图文用 expected_images、order_verified。owned_downloads 每项含绝对 path、sha256、created_by_task:true，仅限本任务新下载文件。未声明的输入原件保留。
3. `adopt "作品链接或本地路径" --media "媒体1" "媒体2" --receipt "回执.json" --title "标题" --author "作者" --caption "原文案"`。分享短链先由宿主解析成最终作品链接。每项返回 job 和完整性结果。源时长未知、错作品、截断、解码失败或图文不全停止此项云调用，批次其他项继续。`integrity --job JOB` 可重新验证。
4. `preview --jobs JOB1 JOB2 --question "理解问题"`：auto 间隔随时长平方根增长，均匀+全片每分钟场景候选+画面去重；逐分钟最多8图一组。重要片段补帧：写 job/extra-frames.json 时间秒数数组后重新 preview。音频超过300秒时尽量在最后5秒内静音处分段，覆盖全片，记录起点偏移。完整性、分段图片及音频/请求上限写入 out/plans/ID.json；重复 job 需宿主按ID/哈希去重。已完成任务预览零新增调用。
5. 展示作品清单、时长、每段覆盖、图片数、模型、ASR缓存和新增调用上限。下游文字摘要无法预知完全相同输入，按最坏新增次数预留，实际命中缓存不再收费。用户确认一次后 `run --plan PLAN --approve ID`；已有持续授权在范围内有效。新素材/扩大范围必须更新预览。
6. 全音频转写保持原生时间与偏移，图像实际分析之后再结合语音证据逐分钟理解，长结果按十段分层汇总，最终报告没有1800字硬限制。视觉仍是采样覆盖，必须说明未逐帧观看。`resume --plan PLAN --approve ID` 复用缓存，未决请求先核对，不能自动重发。
7. run 返回 review_ready。宿主查看关键原帧、数字、代码/公式和图文顺序，在 analysis.md 修订，并写 review.json：`{"status":"sampled","analysis_sha256":"报告SHA256","checks":[{"evidence":"f00001","observation":"实际观察与修订"}]}`。再 `finalize --job JOB`。完成后 `validate --job JOB` 和 status 可在没有媒体时运行。
8. 可选 `search --job JOB --query "待核实事实"`，优先元宝再博查；阅读来源后把外部核查单列，搜索结果不自动作为作品事实。清理不删除账本、未决请求或用户原件。

运行/结果/缓存/审计只留 MD/JSON。metadata/frames 中历史文件路径仅作取得审计，报告用作品URL、时间、图号、哈希和文字观察。迁移及恢复见 recovery.md。新作品进入同一流程；宿主按作品ID/媒体哈希归并批次并保留失败清单。
