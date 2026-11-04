# xiaohongshu operation guide

## Validation scope
See the observations below for the actual v2.4 control/flow scope. TikTok is supplied as an untested workflow this round. Historical Douyin Codex cases and WorkBuddy 5.9.3 page-reading evidence do not establish current end-to-end success.

## Procedure
1. Use the host's actual browser to open the selected feed/search/work page. Verify URL, author, work ID, title and duration/image count. The user handles login/CAPTCHA.
2. Inspect live roles/names/labels/titles for search, play/pause, mute, progress, next work and image arrows. Record semantics and state; never guess tool names.
3. Verify mute after clicking it. Read actual playback progress, wait at normal speed and confirm completion before advancing. Load [vision](../vision.md) for missing semantics.
4. For image posts inspect current index/total and visit all in original order. Unknown completeness blocks paid deep analysis.
5. Prefer verified free parsers. Discover sources through existing search skills, host search, then Yuanbao/Bocha. Verify landed files and integrity; record failures as deferred.

## Evidence and recovery
Control maps record host/browser/extension versions, page type, observation time, locator basis, before/after states and sanitized evidence. Only reviewed generic semantics enter public guides; account/content stays local. Reinspect changed controls; preserve deferred work and continue independent items when vision fails.


## Observed controls

2026-11-04 Windows Codex Chrome: the initial search placeholder was 登录探索更多内容. Later page state changed; re-read DOM rather than retaining stale selectors. Detail images used `.swiper-slide-active img` and `.swiper-slide:not(.swiper-slide-duplicate) img`. Carousel clones do not count as original images. The observed single-image sample contained three page previews within one image, not three post images.
