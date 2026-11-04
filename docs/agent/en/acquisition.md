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

[ZIP acquisition, order review and complete receipt examples](zip-images.md).

## Expected outputs and success evidence

Readable media, an acquisition receipt and integrity results. Video checks identity/duration/decode/head-tail; image posts check count/content/order. Mark a parser successful only after integrity passes.

## Stop or recovery conditions

Unknown/mismatched identity, duration or order, decode/security failures, login/CAPTCHA blocks or exhausted round limits stop paid understanding for that work. Record the restriction; independent works may continue under [recovery](recovery.md).

## Next links

After successful acquisition, preview through the [workflow](workflow.md). For failures or temporary files left behind, read [recovery](recovery.md).


v2.4: prefer installed Git Bash, then PowerShell 7, then Windows PowerShell 5.1; record actual executable/version. New WorkBuddy installs use user-level `.workbuddy/skills/douyin-agent`; existing receipt paths remain. Separate session folder from runtime workspace. Use system UTC observations. Load [browsing](browse.md) for platform/vision routes. Prefer free parsers for acquisition; discover sources through existing search skills, host search, then configured Yuanbao/Bocha. Guide local Key setup only when search capability is missing. `parsed_download_failed` means parsing succeeded but no file landed. Every attempt counts toward the three-source round limit. User-assisted imports preserve originals and require identity, head/tail, duration or image-order checks. Avoid reading unknown clipboard contents for download links.
