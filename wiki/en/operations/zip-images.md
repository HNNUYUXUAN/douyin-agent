---
{
  "type": "Runbook",
  "title": "When individual image downloads fail: acquire a ZIP",
  "description": "When individual image downloads fail: acquire a ZIP — douyin-agent operational knowledge",
  "tags": [
    "douyin-agent",
    "en",
    "operations",
    "zip-images"
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

# When individual image downloads fail: acquire a ZIP

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
    route='parser'
    provider='https://PARSER_PUBLIC_HOST/'
    round_id='CURRENT_WORK_ROUND'
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


Replace provider, host and round_id with the actual attempting receipt registered before parser access. User import uses route=user_import and preserves original ZIP/images.


## User-imported ZIP / 用户导入 ZIP

For a user-provided original ZIP use `route=user_import` and `import_manifest`, pointing to the workspace JSON generated by `unpack_images.py`. `owned_artifacts` may list verified extracted copies, excluding the original ZIP. The script verifies archive/image hashes, directory and image set, then records protected originals.
