# Search, acquisition and completeness

[中文](../zh-CN/acquisition.md) · [Index](../index.json)

## Applicable intent

Find the original work from a topic, link or share text, then obtain and verify video or ordered images, including ZIP acquisition when individual downloads fail.

## Prerequisites

The selected browser is connected and can access the original work; the host has download and local-media inspection capabilities. Follow user authorization and the ownership rules below.

## Minimum inputs

A topic or original work URL and expected source identity. Video needs reliable source duration; images need original count/order. ZIP processing also needs the downloaded archive, expected count and a new workspace output directory.

## Procedure

The host operates a connected Chrome/Edge. The CLI starts with `adopt` and actual media; it is neither a universal Douyin downloader nor a site keyword-search tool. See [README](../../../README.en.md) for system relationships and the [acquisition contract](../../../references/browser.md) for details.

1. For a topic, search Douyin through the host and present verifiable candidates. Resolve share text/short links to the canonical work page first. Check the actual work ID, author, title, complete caption, duration or image count. Recommendation cards and webpage AI summaries are not the work.
2. Prefer methods already verified on this host. `providers` reads the local registry. Use host download for directly accessible media; for blob/failure try a verified free parser. If that fails, the host searches for new public free sources. Try at most three distinct sources per round with one `round_id`.
3. Submit only public work links to a parser. Do not provide cookies, accounts or Keys, pay automatically or install plugins. Record login requirements, CAPTCHA, quota exhaustion and unavailable services separately. Do not create repeated rounds to bypass a real restriction. Acquisition failure affects only that work.
4. Compare page duration with local probe duration, allowing the greater of one second or two frame durations. Check video/audio tracks, full decode and real head/tail frames. Record silence/missing audio accurately; do not fabricate speech. Missing reliable source duration means unknown, not complete. Check image count, original order, coverage and caption.
5. Mark a provider successful only after integrity passes. `providers --receipt FILE` accepts `url`, `search_source`, `host`, `instructions`, `types`, `outcome` and `round_id`; successful receipts also identify the actual `job`. Use clean public HTTPS entry URLs without queries or credentials. Never retain signed media URLs, scripts or download tokens.
6. Hand off the acquisition receipt through `adopt` as described in the [workflow](workflow.md). Record exact absolute paths, SHA256 and acquisition method. `owned_downloads` lists newly downloaded actual inputs; `owned_artifacts` may list verified task-owned acquisition media/ZIPs. Both require `created_by_task:true` and matching hashes. Preserve user originals by default.

A successful source is evidence for that verified host/work, not a guarantee of future availability or universal support. Report deleted, private, paid, live or persistently incomplete works as restricted. A readable page, playable player or visible download button alone does not prove complete media acquisition.

### When individual image downloads fail: acquire a ZIP

If individual images cannot be downloaded, the host may try another public free parser's bulk ZIP option within the three-source round limit. This ZIP is temporary acquisition input, not an archive delivered to the user, and no parser is a required dependency. A page saying packaging succeeded does not prove that the ZIP downloaded or that its images are complete. Record failures as failures.

First establish the actual image count and carousel order on Douyin. Download the ZIP through the host and record its absolute path, SHA256 and acquisition evidence. This nine-image example requires replacing the workspace, actual ZIP path and expected count. The archive must already exist; `--output` must be a **new, nonexistent** short ASCII subdirectory inside the workspace. Pass absolute paths.

```powershell
# Replace this path with the actual workspace context file.
$ctx = Get-Content -LiteralPath 'D:\douyin-agent\agent-context.json' -Raw | ConvertFrom-Json
$archive = Join-Path $ctx.workspace 'out\acquire\note.zip'
$imageDir = Join-Path $ctx.workspace 'out\acquire\note-img'
& $ctx.python (Join-Path $ctx.skill_root 'scripts\unpack_images.py') --archive $archive --workspace $ctx.workspace --output $imageDir --expected-images 9
```

Before creating output, `unpack_images.py` validates every entry and rejects traversal, links/special files, encryption, excessive expansion, non-images and images that cannot fully decode. It writes files named by their actual format, such as `i001.jpg/png/webp/bmp`, plus `manifest.json`. Do not use a general extractor to expand untrusted archive paths directly.

The manifest's `order_basis` is natural filename sorting and its `order_verified` is false: **sorting does not establish the work's order**. The host must compare every image with the original page for identity, count, content and position. If needed, reorder the path array passed to `--media`. Do not assert `order_verified:true` or start paid understanding before this check.

The following receipt example builds the complete ZIP-and-images list from the manifest. Replace the work ID/URL, host and count; verify that each listed file was acquired/created by this task. Pass the actual title, author and caption through adopt's corresponding options when available. Example passed flags do not substitute for actual review.

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

`owned_downloads` still accepts only newly downloaded files that are actual `--media` inputs; it cannot include a ZIP. `owned_artifacts` accepts task-owned acquisition media or ZIPs, each with absolute `path`, actual `sha256` and `created_by_task:true`. It may list the archive and all extracted images as above. Never mark user-provided original ZIPs/images as task-owned: preserve an imported ZIP and register only the extracted copies created by this task. The JSON manifest remains a text audit artifact and must not enter owned_artifacts.

Adopt copies the images into the job and runs integrity checks. Only after a pass may `providers --receipt FILE` mark that source successful. Continue with the [workflow](workflow.md): preview, understand, review and finalize. Cleanup removes job media plus the registered temporary ZIP and extracted images, retaining the text manifest/receipt and results. If acquisition fails before adopt, finalize cannot discover unregistered files; the host must retain exact acquisition records and handle proven ownership file by file, never clear a Downloads or extraction directory.

## Expected outputs and success evidence

Readable media, an acquisition receipt and integrity results. Video checks identity/duration/decode/head-tail; image posts check count/content/order. Mark a parser successful only after integrity passes.

## Stop or recovery conditions

Unknown/mismatched identity, duration or order, decode/security failures, login/CAPTCHA blocks or exhausted round limits stop paid understanding for that work. Record the restriction; independent works may continue under [recovery](recovery.md).

## Next links

After successful acquisition, preview through the [workflow](workflow.md). For failures or temporary files left behind, read [recovery](recovery.md).
