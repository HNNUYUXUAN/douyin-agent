---
{
  "type": "Runbook",
  "title": "Dependency and parser-file transfer",
  "description": "Dependency and parser-file transfer",
  "tags": [
    "douyin-agent",
    "en",
    "transfer",
    "v251-runtime"
  ],
  "status": "active",
  "generated": {
    "by": "douyin-agent/2.5.1",
    "at": "2026-11-05T15:06:20.335700+00:00"
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

# Dependency and parser-file transfer

Trigger: slow dependency transfer, TLS segment failures, parser results without saved media, error bodies named as media, or staging buildup. Applies to the v2.5.1 candidate; check the original receipt and round first.

`da.py --workspace WORKSPACE providers --platform douyin` returns registered exact entries. Douyin SnapAny uses /zh/tiktok; never synthesize paths. Reuse verified free sites, then discover through existing search skills, host search and configured Yuanbao/Bocha. Each work/round allows three distinct sites, including login walls, CAPTCHAs and failures. Keep the same round across transport changes; one failed site is not exhaustion.

Use UTF-8 JSON (BOM accepted) with `providers --receipt FILE.json` or `providers --batch ARRAY.json`. All batch items validate before a replayable commit. The first receipt generates attempt_id, retained across updates. Adopt actual media with route=parser and its source linkage; passed integrity closes success automatically. Transfer failures are parsed_download_failed; no observed work result is no_result; explicit unsupported results are failed. Report unclosed attempting items at handoff.

Save only files returned by parsers, through available browser/download skills. For curl use `PYTHON SKILL/scripts/transfer.py --workspace WORKSPACE save --url-stdin --provider-receipt SOURCE.json --output out/file.mp4 --kind video`, supplying the current actual HTTPS file URL via stdin. There are no Cookie/custom UA/Referer options. Save temporarily, verify size/type/SHA256/full decode, then publish the final name. A 403 body cannot become a successful mp4. Never cycle proxies after explicit denial. Receipts live in out/transfers; successful segment staging retires automatically. On explicit termination, `... cleanup --id ID` removes hash-verified task artifacts and retains text receipts; changed files stay.

Windows dependency bootstrap without Python:
```text
powershell.exe -NoProfile -File SKILL/scripts/download-dependency.ps1 -Workspace WORKSPACE -Url OFFICIAL_URL -Output out/dependency.exe -Sha256 EXPECTED_SHA256
```
Only registered official-listed origins with a full expected SHA256 are accepted. Slow/time-limited whole transfers may fall back to at most eight ranges, checking 206, Content-Range, lengths and stable ETag/Last-Modified. Retry only failed segments once, then check the complete digest. Keep TLS validation and one origin/version. Unsupported ranges, resource changes or digest errors stop with evidence. After installation and independent availability verification, use `-Cleanup -Workspace WORKSPACE -Output TRANSFER_ID` to clean owned installers/staging, preserving environments/source.

Success requires an actual complete file and source/identity/duration/image-order evidence; dependency version/signature checks remain required. Limit to three sites and one failed-segment retry. Retain blocked items and the user-import route. Distinguish slow, intermittent and denied access; one short timeout never proves permanent unreachability.
