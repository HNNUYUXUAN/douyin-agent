---
{
  "type": "Runbook",
  "title": "youtube operation guide",
  "description": "youtube operation guide — douyin-agent operational knowledge",
  "tags": [
    "douyin-agent",
    "en",
    "platforms",
    "youtube"
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

# youtube operation guide

## Validation scope
See the observations below for the actual v2.4 control/flow scope. TikTok is supplied as an untested workflow this round. Historical Douyin Codex cases and WorkBuddy 5.9.3 page-reading evidence do not establish current end-to-end success.

## Procedure
1. Use the host's actual browser to open the selected feed/search/work page. Verify URL, author, work ID, title and duration/image count. The user handles login/CAPTCHA.
2. Inspect live roles/names/labels/titles for search, play/pause, mute, progress, next work and image arrows. Record semantics and state; never guess tool names.
3. Verify mute after clicking it. Read actual playback progress, wait at normal speed and confirm completion before advancing. Load [vision](../operations/vision.md) for missing semantics.
4. For image posts inspect current index/total and visit all in original order. Unknown completeness blocks paid deep analysis.
5. Prefer verified free parsers. Discover sources through existing search skills, host search, then Yuanbao/Bocha. Verify landed files and integrity; record failures as deferred.

## Evidence and recovery
Control maps record host/browser/extension versions, page type, observation time, locator basis, before/after states and sanitized evidence. Only reviewed generic semantics enter public guides; account/content stays local. Reinspect changed controls; preserve deferred work and continue independent items when vision fails.


## Observed controls

2026-11-04 Windows Codex Chrome: search uses role=combobox and Search button. Observed player labels included 暂停 (k), 静音 (m), 取消静音 键盘快捷键 m, 重放 and 设置; progress uses role=slider. The speed menu showed normal. A 6.061-second public video played from zero to ended=true muted at rate=1. Completion used live media properties as well as supplementary screenshots.

Acquisition: the first source required Pro; https://getfrom.io/en supplied a complete 720p file free. Player/local duration differed by about 0.023 seconds. Live analysis, review and cleanup passed. Revalidate future source availability.
