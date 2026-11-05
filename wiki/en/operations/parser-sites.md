---
{
  "type": "Runbook",
  "title": "Measured parser routes and file receipts",
  "description": "Measured parser routes and file receipts",
  "tags": [
    "parser",
    "download",
    "解析站",
    "文件回执",
    "bilibili",
    "youtube",
    "xiaohongshu"
  ],
  "status": "active",
  "generated": {
    "by": "douyin-agent/2.5.0",
    "at": "2026-11-05T03:58:14.273533+00:00"
  },
  "sources": [
    {
      "resource": "https://snapany.com/zh/bilibili"
    },
    {
      "resource": "https://snapany.com/zh/tiktok"
    },
    {
      "resource": "https://getfrom.io/en"
    },
    {
      "resource": "https://greenvideo.cc/"
    }
  ],
  "applicability": {
    "skill": "2.5.x",
    "host": "Capabilities rechecked at runtime; measured scope in body"
  }
}
---

# Parser sites and file receipts

Measured on Windows 11 x64 (10.0.26300), connected Chrome 156.0.8078.81 and Codex desktop. Host/connection-extension versions are unknown. These results establish only the named public samples and this run; revalidate each task.

| Parser entry | Successful samples | File evidence |
|---|---|---|
| https://snapany.com/zh/bilibili | BV1dC4y117Rz p1 and BV1Lphuz7E6w p2 | Visible parser video links returned exact host download paths; identity, duration, full decode and head/tail passed |
| Same entry | Dynamic 792155723808112674, one long image | Browser showed403 for the parser image link; existing curl saved HTTP200 without Cookie or extra headers; valid3707×8000 JPEG |
| https://snapany.com/zh/tiktok | Douyin7574366810088148709 | Visible parser file link; after browser save timeout, existing curl saved HTTP200;15.8s media passed identity/duration/head-tail |
| https://getfrom.io/en | YouTube zKYNITx17Mw | 720p selection produced download event/path; valid6.083628s media |
| https://greenvideo.cc/ | Xiaohongshu6aea848900000000030011bf, one contest poster | Existing curl saved the parser-provided image link; valid2448×3264 JPEG |

## Preflight file saving

Probe existing download skills, host download events/link saving and already installed standard transfer tools such as curl. `onboard --check` reporting curl=true proves command discovery only; require a real file receipt. Missing browser download events do not establish that the device cannot save files.

Standard tools transport only public file links actually returned by the selected parser for the correct work. Use explicit task output paths. Do not extract URLs from platform players, cookies or hidden APIs. Do not add account Cookies, private tokens or spoof headers to evade refusals. Verify actual file/hash/integrity; parsing, preparation and file acquisition are separate states. Remove temporary signed URLs after use; keep them out of public knowledge and permanent logs.

## Same-round recovery and limits

At most three distinct parser hostnames per work/round. Different paths or browsers for the same site do not grant/reset allowance. Record attempting before access; login walls, CAPTCHAs, unavailable and parsed_download_failed count. Changing file transport retains the parser and round_id, including prior failures. Do not create another round to evade the limit.

Some GreenVideo/Kedou buttons produced no verifiable path; this does not prove no browser file was saved. Other Xiaohongshu sources gave no actual result or reported automated access blocked for that sample. UI example galleries are not task evidence. Already obtained public links can be transported within the same round.

providers.previously_verified means latest success with route=parser; needs_live_validation always requires current verification. Old platform/CDN receipts remain historical evidence.

## Discovery and retention

Existing search skills/plugins → host-native search → configured Yuanbao/Bocha. If all are unavailable, guide installation/local configuration. Defer failures with user_import available. Clean only receipt-proven task-owned media with matching hashes. Preserve unknown downloads and user-import originals.
