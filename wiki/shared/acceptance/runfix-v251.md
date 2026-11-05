---
{
  "type": "Reference",
  "title": "v2.5.1 runtime repair coverage",
  "description": "Latest 22 feedback items, code and evidence scope",
  "tags": [
    "F251R",
    "runtime",
    "acceptance"
  ],
  "generated": {
    "by": "douyin-agent/2.5.1",
    "at": "2026-11-05T15:11:02.510359+00:00"
  },
  "sources": [
    {
      "resource": "https://requests.readthedocs.io/en/latest/user/quickstart/#timeouts"
    }
  ],
  "applicability": {
    "skill": "2.5.1 candidate"
  },
  "verification_scope": "Per-row scope; final recipient gate pending"
}
---

# v2.5.1 runtime repair coverage / 运行修复映射

Scope: latest I-1–I-8 and R-1–R-14. Original recipient evidence remains local. Historical I codes in field-v251 are a different round; use F251R- prefixes below. Local fixture, live Codex/Chrome, WorkBuddy recipient and final release are separate gates.

| Code | Finding | Implementation/manual | Evidence scope |
|---|---|---|---|
| F251R-I-1 | Slow full download | download-dependency.ps1; transfer.py; [manual](../../en/operations/transfer.md) | Range fixtures |
| F251R-I-2 | Segment TLS | download-dependency.ps1; transfer.py; [manual](../../en/operations/transfer.md) | Bounded failed-segment fixtures |
| F251R-I-3 | PowerShell browser arrays | workbuddy-bridge.ps1; [manual](../../en/operations/runtime-host.md) | PS5/PS7 checks |
| F251R-I-4 | onboard record plus check | da.py; [manual](../../en/operations/runtime-host.md) | CLI compatibility fixtures |
| F251R-I-5 | Stopped user browser | browser-ready.ps1; [manual](../../en/operations/runtime-host.md) | Read-only process checks; launch fixtures passed PS5/PS7 |
| F251R-I-6 | Capture focus | runtime-host.md; [manual](../../en/operations/runtime-host.md) | Host procedure; per-host observation required |
| F251R-I-7 | Inline image versus export | runtime-host.md; [manual](../../en/operations/runtime-host.md) | Separate capabilities; no private temp searches |
| F251R-I-8 | Key waiting | setup_flow.py; [manual](../../en/operations/runtime-host.md) | Existing setup regression |
| F251R-R-1 | Exact parser routes | provider_state.py; [manual](../../en/operations/transfer.md) | Route fixtures and live Bilibili |
| F251R-R-2 | Explicit Chrome preference | runtime-host.md; [manual](../../en/operations/runtime-host.md) | Live Chrome used |
| F251R-R-3 | Login and playback separation | browser_state.py; runtime-host.md; [manual](../../en/operations/runtime-host.md) | Existing login fixture plus page evidence |
| F251R-R-4 | Raw file transport | transfer.py; [manual](../../en/operations/transfer.md) | No custom cookie/UA/referer interface |
| F251R-R-5 | No saved file | save_watch.py; transfer.py; [manual](../../en/operations/runtime-host.md) | File ambiguity and error-body fixtures |
| F251R-R-6 | Empty parser result | da.py; [manual](../../en/operations/transfer.md) | no_result and source limit regression |
| F251R-R-7 | Network classification | transfer.md; [manual](../../en/operations/transfer.md) | Observed denial versus slow/intermittent evidence |
| F251R-R-8 | Vision timeout diagnostics | cloud_transport.py; [manual](../../en/operations/recovery.md) | SSE/header/incomplete fixtures and live cloud |
| F251R-R-9 | Unknown recovery lifecycle | request_state.py; da.py; [manual](../../en/operations/recovery.md) | One retry, reconcile, cache interruptions, abandon |
| F251R-R-10 | One pipeline | da.py locked; [manual](../../en/operations/recovery.md) | Existing workspace lock and progress |
| F251R-R-11 | Batch receipts and BOM | provider_state.py; legacy.py; [manual](../../en/operations/transfer.md) | All-validate-before-commit and transaction replay |
| F251R-R-12 | Unclosed sources | provider_state.py; da.py; [manual](../../en/operations/transfer.md) | Open source overview and automatic terminals |
| F251R-R-13 | Stale nodes | runtime-host.md; [manual](../../en/operations/runtime-host.md) | Semantic and once-relocate procedure |
| F251R-R-14 | Short acceptance pool | docs/agent/samples.json; [manual](../../en/operations/transfer.md) | 5–30 sec requirement; live validity remains explicit |

BOM: JSON readers accept utf-8-sig. Ownership: verified successful transfer staging retires; explicit cleanup/abandon requires matching path and SHA256. Preserve environments, source, imports and unknown files.

Live scope: synthetic image with controlled interruption recovered, reviewed and finalized; a 21.12-second Bilibili P2 parser file was fully decoded, analyzed, sample-reviewed and finalized. Original recipient unknown requests were untouched. YouTube 19.064-second parser file also completed full ASR, vision, sampled review and cleanup. Other platform samples and clean-device candidate acceptance remain separately recorded; this document does not mark them passed. Host points and settled cloud billing are unknown.

Local live timing: YouTube ASR 21.453 s; four vision calls 89.062/46.609/38.453/18.203 s; report 87.172 s. These are individual measured calls, not a latency guarantee or a settled bill. Real native curl process waiting and SHA256 were checked in PS5/PS7 against a 5296-byte official-listed FFmpeg supplier checksum asset; no installer was executed.

Platform gate: two fresh successful samples per each of five platforms are not complete. Douyin returned a parser result then HTTP403, one XHS note was unavailable and its parser explicitly failed; TikTok candidate durations remain unverified. Browser control stopped when its current-URL safety check became unavailable. Preserve these blocked/pending states and use local import for an actual user work when applicable.

Offline result: 121 Python cases passed; targeted recovery/transport cases were repeated after the final diagnostic phase change. PS5.1 and PS7 each passed 26 setup + 31 bridge + 10 transfer + 9 browser/argument assertions. Actual Git Bash/PS5/PS7 placement, upgrade and repeat reused an existing QA environment; they do not prove clean-OS Conda installation. JSON BOM and native -File comma arguments were also exercised.
