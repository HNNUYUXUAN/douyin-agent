# 图文逐张下载受阻：ZIP 批量获取

逐张图片下载受阻时，宿主可以在每轮三个来源的上限内尝试其他公开免费解析站的“一键下载 ZIP”。它是取得阶段的临时输入，不是向用户分发压缩包，也不需要把某个解析站设为必备依赖。解析页面显示“打包成功”不等于 ZIP 下载及图片完整性通过；失败来源按实际失败登记。

先在抖音原页记录实际图片数量和轮播顺序，再通过宿主下载 ZIP，记下绝对路径、SHA256 与取得记录。以下以九图作品演示：把工作区、ZIP 实际路径及图片数量替换为本次值；ZIP 必须已落盘，`--output` 必须是工作区内**尚不存在**的短 ASCII 子目录，参数传绝对路径。

```powershell
# Replace this path with the actual workspace context file.
$ctx = Get-Content -LiteralPath 'D:\douyin-agent\agent-context.json' -Raw | ConvertFrom-Json
$archive = Join-Path $ctx.workspace 'out\acquire\note.zip'
$imageDir = Join-Path $ctx.workspace 'out\acquire\note-img'
& $ctx.python (Join-Path $ctx.skill_root 'scripts\unpack_images.py') --archive $archive --workspace $ctx.workspace --output $imageDir --expected-images 9
```

`unpack_images.py` 在创建输出前检查全部条目，拒绝路径越界、链接/特殊文件、加密、超量膨胀、非图片及无法完整解码的图片；输出按实际图片格式命名的 `i001.jpg/png/webp/bmp` 等文件和 `manifest.json`。不要使用通用解压命令直接展开不明 ZIP 内的路径。

manifest 的 `order_basis` 是自然文件名排序，`order_verified` 固定为 false：**排序不是作品顺序证据**。宿主必须逐张比对原页确认身份、数量、图片内容和位置；顺序不同则调整传给 `--media` 的路径数组。未核验不填写 `order_verified:true`，不进入收费理解。

下列回执示例由 manifest 生成完整的 ZIP＋解包图片清单。先替换作品 ID/URL、宿主名和数量，并确认每个文件都是本任务新取得/生成的；真实标题、作者、文案可继续传给 adopt 对应参数。不要直接执行示例中的通过状态来代替复核。

```powershell
# Run only after the host has verified the original page and all image positions.
# Every listed file must be created by this task, not a user-imported original.
$manifest = Get-Content -LiteralPath (Join-Path $imageDir 'manifest.json') -Raw | ConvertFrom-Json
$owned = @(@{path=$manifest.archive.path; sha256=$manifest.archive.sha256; created_by_task=$true})
$owned += @($manifest.images | ForEach-Object {
    @{path=$_.path; sha256=$_.sha256; created_by_task=$true}
})
$receipt = @{
    source_id='7699716622642105615'
    identity_verified=$true
    expected_images=9
    order_verified=$true
    method='free_parser_zip'
    host='Windows Codex Chrome'
    owned_artifacts=$owned
}
$receiptPath = Join-Path $ctx.workspace 'out\acquire\note-receipt.json'
$receipt | ConvertTo-Json -Depth 6 | Set-Content -LiteralPath $receiptPath -Encoding utf8
# Use this order only if it matches the original carousel; otherwise set an explicitly reviewed order.
$imagePaths = @($manifest.images | ForEach-Object { $_.path })
& $ctx.python (Join-Path $ctx.skill_root 'scripts\da.py') --workspace $ctx.workspace adopt 'https://www.douyin.com/note/7699716622642105615' --media $imagePaths --receipt $receiptPath
```

`owned_downloads` 仍仅接受实际 `--media` 输入中的新下载文件，不能放 ZIP。`owned_artifacts` 接受取得过程中任务拥有的媒体或 ZIP，逐项要求绝对 `path`、实际 `sha256`、`created_by_task:true`；可以像上例登记 ZIP 和全部解包图片，不能把用户提供的原始 ZIP/图片标为任务所有。用户导入 ZIP 应保留原件，仅登记本任务产生的解包副本。JSON manifest 是长期取得审计，不放进 owned_artifacts。

adopt 复制图片到 job 并运行完整性检查；只有通过后才用 `providers --receipt FILE` 把对应来源登记成功。之后按 [任务流程](workflow.md) 预览、理解、复核并 finalize：清理 job 内媒体、已登记的临时 ZIP 与解包图片，只保留文字 manifest/回执与结果。若在 adopt 前失败，尚未归属 job 的下载物不会被 finalize 自动发现；宿主须保留精确取得记录并按所有权逐文件处理，不清空下载或解包目录。

