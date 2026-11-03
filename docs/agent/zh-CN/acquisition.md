# 检索、取得与完整性

[English](../en/acquisition.md) · [索引](../index.json)

## 适用意图

根据主题、链接或分享文案找到原作品，取得并核验视频或有序图文；包括逐张下载受阻后的 ZIP 获取。

## 前置条件

所选浏览器已连接且能访问原作品；宿主具备下载和本地媒体检查能力。取得/下载仍需遵循用户授权及下文所有权规则。

## 最少输入

主题或原作品链接、预期作品身份；视频需可靠源时长，图文需原图数量与顺序。ZIP 流程另需已下载档案、预期数量及新的工作区输出目录。

## 操作步骤

由宿主使用已连接的 Chrome/Edge 操作网页；CLI 从实际媒体的 `adopt` 开始，不提供通用抖音下载器或站内关键词搜索。系统关系与主链路见 [README](../../../README.md)，完整协议见 [取得协议](../../../references/browser.md)。

1. 用户给主题时，宿主在抖音站内搜索并展示可核对的候选。给分享文案/短链时，先在浏览器解析到最终作品页。直接确认作品 ID、作者、标题、完整文案、时长或图文数量，不以推荐卡片或网页 AI 摘要代替作品。
2. 优先复用当前宿主已验证的获取方式。`providers` 读取本机来源记录。直接媒体可下载时使用宿主下载；遇到 blob 或失败再尝试已验证的免费解析来源，失效时由宿主搜索新的公开免费来源。每轮最多三个不同来源，以同一 `round_id` 记账。
3. 只向解析站提交公开作品链接；不提供 Cookie、账号、Key，不自动付费或安装插件。登录、验证码、额度耗尽、来源失效分别记录，不能靠重复轮次绕过实际受限。获取失败仅影响该作品。
4. 视频核对页面时长与本地探测时长，允许差为一秒或两个帧时长的较大值。检查视频/音频轨、全片解码和真实首尾画面。静音/无音轨须按实际记录，不能编造转写；缺少可靠源时长为未知，不宣称完整。图文核对实际数量、原顺序、覆盖范围与文案。
5. 仅完整性通过，才可把来源标记成功。`providers --receipt FILE` 回执字段：`url`、`search_source`、`host`、`instructions`、`types`、`outcome`、`round_id`；成功时加实际 `job`。URL 使用无查询串/凭据的公开 HTTPS 服务入口；不得保存签名下载地址、脚本或令牌。
6. 取得回执与 `adopt` 交接详见 [任务流程](workflow.md)。记录新下载文件的绝对路径、SHA256 和取得方式；`owned_downloads` 仅登记实际输入的新下载副本，`owned_artifacts` 可登记已核验的任务临时媒体/ZIP。均须 `created_by_task:true` 与哈希匹配，用户原件默认保留。

来源成功只对已核实的宿主、当次作品成立，不保证该服务将来可用或支持任何作品。删除、私密、付费、直播及始终无法完整取得的作品应报告受限。浏览器页可读、播放器可播放、下载按钮存在，都不能单独证明完整媒体已取得。

### 图文逐张下载受阻：ZIP 批量获取

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

## 预期输出与成功依据

得到可实际读取的媒体、取得回执及完整性结果。视频核对身份/时长/解码/首尾；图文核对数量/内容/顺序。解析来源只有在完整性通过后才登记成功。

## 停止或恢复条件

身份、时长或顺序未知/不符、解码或安全校验失败、登录/验证码阻断、每轮来源用尽时，记录该作品受限并停止收费理解；其他独立作品按 [恢复指南](recovery.md) 继续。

## 下一步链接

取得通过后进入 [任务流程](workflow.md) 的预览；失败或已留下临时文件时读 [恢复指南](recovery.md)。
