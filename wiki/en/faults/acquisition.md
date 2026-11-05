---
{
  "type": "Runbook",
  "title": "Parser results, empty results and file acquisition faults",
  "description": "Parser results, empty results and file acquisition faults",
  "tags": [
    "acquisition",
    "fault",
    "troubleshooting",
    "故障"
  ],
  "status": "stable",
  "generated": {
    "by": "douyin-agent/2.5.1",
    "at": "2026-11-05T09:44:27.533063+00:00"
  },
  "sources": [
    {
      "resource": "../../shared/acceptance/field-v251.md"
    },
    {
      "resource": "https://github.com/GoogleCloudPlatform/knowledge-catalog/blob/62432a095456147ee71e70ac6e4dc0d2dea3ac30/okf/SPEC.md"
    }
  ],
  "applicability": {
    "skill": "2.5.1 candidate",
    "host": "Windows x64; recheck current host capabilities"
  },
  "verification_scope": "Candidate implementation; fixture, local and recipient results are recorded separately."
}
---

# Parser results, empty results and file acquisition faults

Trigger: no download primitive, advertising-only results, 403 files, or parsed work without a saved file. Scope: free parsers. WorkBuddy 5.9.3 field evidence observed GreenVideo Bilibili browser saving succeed and SnapAny video links fail with 403; this is not a permanent guarantee.
Preconditions: after explicit start probe host download, installed download skills, existing curl and exact-file receipt capability. Tool presence is not saving proof. Reuse verified parsers; discover replacements through existing search skills → host search → configured Yuanbao/Bocha.
Procedure:
1. Each work's original round allows three distinct sites. Record attempting before access; changing path/browser/transport keeps the round/site. Login, CAPTCHA and failures count. First-site failure is not exhaustion; never automatically open another round.
2. Type and read back. After waiting, advertising/no work result is no_result, which proves neither parsing success, throttling nor permanent failure. Continue within remaining sites.
3. Correct parsed work but failed saving is parsed_download_failed. WorkBuddy Bilibili can prefer a currently verified parser-button → user-browser download. Do not extract from the native player.
4. Existing tools may save an actual public parser file link. Do not retry an explicit 403 through proxy switching/spoofed headers. A browser download is a distinct transport within the same site/round. If the site explicitly requires a desktop client, move to the next site rather than install it.
5. Without download events, verify the task-click's exact filename, time, size and hash. Do not adopt/delete unknown files, sweep Downloads or read unknown clipboard contents.
Success: actual file, identity, integrity, duration/image order; separate parse and acquire results. route=parser requires provenance. Only actual user imports use user_import; a proposed import is not success.
Bounds: three sites in the original round, one justified transport recovery per site. Do not repeat the same refusal. Pending paid calls follow their separate recovery contract.
Stop/resume: defer with local-import entry when exhausted or no saving route; preserve originals.


Current runtime procedure / 当前运行流程：[v2.5.1](../operations/transfer.md).
