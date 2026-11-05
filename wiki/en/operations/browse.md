---
{
  "type": "Runbook",
  "title": "Finite browsing and session authorization",
  "description": "Finite browsing and session authorization — douyin-agent operational knowledge",
  "tags": [
    "douyin-agent",
    "en",
    "operations",
    "browse"
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


# Finite browsing and session authorization

## Preconditions and selection
Start only after an explicit user request. Verify host browser, files and terminal; load [platforms](platforms.md), [vision](vision.md) and [acquisition](acquisition.md) as needed. No resident process or scheduler is installed.
Ask once for missing platform, entry/topic, mode, selection criteria, time/item limits, image dwell and cloud limits. Modes browse, selective and all are equal choices with no default. Reuse fields already supplied by the user. Browsing can still require visual assistance; unreadable host token usage stays unknown.

The following is a format example, not spending authorization. Replace every value with the user's choices:
```json
{"platforms":["douyin"],"mode":"browse","entry":"current recommendations","selection":"","max_seconds":600,"max_items":3,"image_dwell_seconds":3,"limits":{"requests":0,"images":0,"audio_seconds":0,"search_requests":0}}
```
At least one time/item bound must be positive; explicitly use null for an unused bound. Zero cloud limits allow DOM-only work without new skill cloud requests.

## Commands and execution
Prefix commands with `PYTHON SKILL/scripts/da.py --workspace WORKSPACE`, using actual local paths.
```text
browse create --config CONFIG_JSON
browse approve --session SID --approve APPROVAL_ID
browse status --session SID
browse record --session SID --file OBSERVATION_JSON
browse pause --session SID
browse resume --session SID --approve APPROVAL_ID
preview --jobs JOB --session SID --question QUESTION
search --session SID --query QUERY
```
create returns a pending session and approval_id. Present its concrete configuration and approve only under applicable user authorization. Resume requires an explicit user request. The host performs browser actions; local code records observations and limits. The host also pauses the player when pausing a session.

Before each work verify platform/ID, identity and duration, and read status. Do not start a known duration exceeding remaining session time. Mute, play once from the beginning at normal speed, and verify progress/end before advancing. Use available host waiting mechanisms in interruptible intervals; avoid per-second screenshots or model polling. Visit all post images in original order with the chosen dwell.

Observation JSON requires source and status (played/observed/deferred), optionally title/observation/reason. Selected works carry selected:true and selection_basis. played requires playback fields muted:true, rate:1, seeked:false, duration/start/end/elapsed_seconds, based on actual observation. Image posts record images and images_visited. Code validates evidence structure rather than measuring the browser. Playback and page observation are distinct from complete-media understanding.

Acquire and integrity-check media, record it, then produce a concrete --session preview. Run under the session's existing scope and remaining allowance without per-item approval. Save over-budget work as pending. Authentication/quota/unresolved issues suspend the affected cloud route and retain reservations; independent DOM steps continue. Record acquisition/control/vision failures as deferred with exact reasons and collect user actions at the end. No automatic retry of unresolved requests.

## Results and recovery
out/sessions/SID/session.json retains configuration, observations and state; usage is calculated from the ledger. Media jobs still require review_ready, actual frame review, finalize and completed. Retain MD/JSON; clean only owned, path/hash-verified media/screenshots and preserve imported originals. Read current state on stop/resume rather than inferring from history.


## Playback and platform blockage

Disable task autoplay before muted sequential playback at normal speed. Click/wait for placeholders or 00:00, inspect same-site players, then network or visible blocking evidence. Do not close user tabs. Without a canonical work ID, `browse record` accepts platform entry source, status=deferred and reason into pending; this does not consume work count or authorize analysis. New approval IDs bind session and config; old sessions remain readable.

[Recovery / 恢复](browser-recovery.md)


Platform values: douyin, youtube, xiaohongshu, tiktok, bilibili.
