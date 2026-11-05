---
{
  "type": "Runbook",
  "title": "Bilibili: videos, parts and image dynamics",
  "description": "Bilibili: videos, parts and image dynamics — douyin-agent operational knowledge",
  "tags": [
    "bilibili",
    "哔哩哔哩",
    "BV",
    "分P",
    "dynamic",
    "图文"
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

# Bilibili: videos, parts and image dynamics

## Source identity

Accept BV video links with optional `?p=N`, av shares, `b23.tv`, `t.bilibili.com/ID` and `www.bilibili.com/opus/ID`. Resolve av/short links through the visible host browser to BV or dynamic identity. Video identity is `bilibili:BV…-pN`; omitted p means p1. Verify title/duration and session allowance for each selected part. Traversing all parts requires user scope. Dynamic identity is `bilibili:dynamic-ID`.

## Pages and controls

Use current visible DOM/semantic controls to verify title, uploader, selected part, duration or image count. Reobserve play, mute, progress, autoplay and next-part controls on each page. Without current local evidence keep selectors unverified. After first play wait a few seconds and inspect progress; a placeholder does not establish extension blocking. Play one task video at a time, muted at normal speed without seeking, recording elapsed time/end/loop evidence.

Open all post images in their original order using the chosen session dwell rule. Distinguish thumbnails, body images and reposted content. Record repost commentary separately from original-work link/visible content. Text-only dynamics are page observations. Video dynamics resolve to the linked BV with relationship evidence.

## Acquisition and recovery

Submit public links to free parser sites and record provider attempts, saved files and integrity. Verify all images/order and the actual selected part. A cover-only, first-part-only or partial-image result is incomplete. Defer unavailable works and offer user import.

Record login, 412, CAPTCHA, deleted, paid and live restrictions separately. Anonymous interface extraction in field feedback remains historical evidence; this version uses parsers. Logged-in sessions support browsing/identity checks rather than media extraction.

## Verification scope

Field evidence: Windows Server 2022, WorkBuddy 5.9.3, extension 0.2.8; BV1dC4y117Rz page and 1080P playback initialization passed, while media came from an anonymous interface. This does not validate this release's parser, multipart or dynamic flow. See release acceptance for current measurements.


[Acquisition / 获取](../operations/acquisition.md) · [Browsers / 浏览器](../operations/browser-selection.md)


## Local controls / 本机控件

Local Chrome 156: semantic Play/Pause and Volume controls; visible volume 0 establishes effective mute even when video.muted is false. P2 showed (2/3), P2, 00:22; acquired duration 21.12s. The current dynamic had one `.b-img__inner img`; “six regions” in its text was not its image count. Reobserve selectors every run and distinguish playback completion from page observation.
