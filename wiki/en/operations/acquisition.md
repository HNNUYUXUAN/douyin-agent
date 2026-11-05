---
{
  "type": "Runbook",
  "title": "Acquire media through free parser sites",
  "description": "Acquire media through free parser sites — douyin-agent operational knowledge",
  "tags": [
    "parser",
    "download",
    "解析站",
    "下载",
    "user_import"
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

# Acquire media through free parser sites

## Preconditions

Verify the public work identity, reliable duration or total image count/order. Probe actual file saving and exact local path reporting before trying providers. Record `host_download_unavailable` when saving is unavailable; offer local user import and continue independent works. Readable pages, successful parsing and saved files are separate observations.

## Discover and try providers

Use `providers` to reuse a free parser verified for this host/platform. Discover alternatives through existing search plugins/skills → host-native search → configured Yuanbao/Bocha. If none is available, guide installation or official service setup with local Key entry. Search results are candidates requiring live verification.

Platform accounts support ordinary browsing, identity checks and public link collection. Acquire media through parser sites; existing download tools only save their results. Submit public links only. Record account, cookie, payment or extra-extension requirements as blocked and offer user import.

Use one stable work-specific `round_id`. Record `outcome=attempting` before visiting a parser. At most three distinct sources per round; login, CAPTCHA, unavailable services and failed saves all count. Do not automatically start another round. Provider `url` and `search_source` are clean public HTTPS entry URLs. Update the same round after completion.

## Receipts and integrity

New `adopt` receipts use `route=parser|user_import`. Parser receipts include `provider`, `host`, `round_id`, matching an already recorded provider attempt. `provider` is the parser entry URL. Preserve originals for `user_import`; do not register them in `owned_downloads`.

For video verify identity, tracks, full decode, duration and actual head/tail. For image posts verify every image, count and original order. A parser-provided ZIP follows the safe ZIP guide before image review. Mark a provider `success` only after the file exists and integrity passes; associate the actual `job`.

Use `parsed_download_failed` for parsing without a saved file. Distinguish login, CAPTCHA, quota, unavailable and other failures. Do not inspect unknown clipboard contents. Signed download URLs are ephemeral transport data and stay out of durable provider records.

Register task-created files with absolute path, SHA256 and `created_by_task:true`. After review, clean registered media/screenshots and retain MD/JSON, receipts, usage, recovery evidence and user originals. Historical receipts remain readable for recovery.


[任务命令 / Task commands](workflow.md) · [ZIP images](zip-images.md)

[File-save preflight and same-round standard transport](../operations/parser-sites.md). Existing curl can save public parser-result files; probe it separately from browser download APIs.
