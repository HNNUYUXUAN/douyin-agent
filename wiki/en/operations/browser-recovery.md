---
{
  "type": "Runbook",
  "title": "WorkBuddy browser failure branches",
  "description": "WorkBuddy browser failure branches — douyin-agent operational knowledge",
  "tags": [
    "WorkBuddy",
    "extension",
    "扩展",
    "offline",
    "离线",
    "screenshot",
    "截图",
    "timeout",
    "超时",
    "provider invocation timed out",
    "Current display surface not available for capture",
    "native messaging"
  ],
  "status": "active",
  "generated": {
    "by": "douyin-agent/2.5.0",
    "at": "2026-11-05T02:27:48.555869+00:00"
  },
  "sources": [
    {
      "resource": "https://gitcode.com/yuxuan6426/workbuddy-browser-bridge-okf/tree/779e3794e495293af3607f66f67a90d6832511b9"
    },
    {
      "resource": "https://developer.chrome.com/docs/extensions/develop/concepts/native-messaging"
    },
    {
      "resource": "https://learn.microsoft.com/en-us/microsoft-edge/extensions/developer-guide/native-messaging"
    }
  ],
  "applicability": {
    "skill": "2.5.x",
    "host": "capability-detected; see body for measured versions"
  },
  "verification_scope": "Documentation reviewed; runtime acceptance is recorded separately."
}
---

# WorkBuddy browser failure branches

## Entry and applicability

Distinguish extension offline / “WorkBuddy is not running”, DOM working with screenshot timeout, and a single page/player not loading. Field recovery evidence covers Windows x64, WorkBuddy 5.9.3 and extension 0.2.8. Check compatibility for other versions; new-helper live coverage belongs in release acceptance.

## Extension offline

Inspect the runtime, `com.workbuddy.extension` manifest, actual extension ID, each browser's HKCU NativeMessagingHosts registration and current host logs. Host-process availability and extension connection are separate facts.

Default `Check` is read-only with no download. `Plan` reads the official feed and previews changes. `Repair` selects an entry compatible with the observed host version, downloads only from the official domain and verifies SHA256, package version and Tencent Authenticode signatures. It backs up affected files/registry entries, merges the selected plugin configuration and records before/after fingerprints. Concurrent edits stop replacement. Register only browsers in use and actually observed official extension IDs.

Replace paths, version and extension ID with actual observations. Prefer PowerShell 7, otherwise Windows PowerShell 5.1. Run from the actual skill root:

```powershell
./scripts/workbuddy-bridge.ps1 -Mode Check -Browser Chrome,Edge
./scripts/workbuddy-bridge.ps1 -Mode Plan -Browser Chrome -WorkBuddyVersion '5.9.3' -ExtensionId 'ajnnogdfpilbhkeggdjlcokgglijmdde' -Receipt 'D:\da\ops\bridge-01.json'
./scripts/workbuddy-bridge.ps1 -Mode Repair -Browser Chrome -WorkBuddyVersion '5.9.3' -ExtensionId 'ajnnogdfpilbhkeggdjlcokgglijmdde' -Receipt 'D:\da\ops\bridge-01.json'
./scripts/workbuddy-bridge.ps1 -Mode Rollback -Receipt 'D:\da\ops\bridge-01.json'
```

Wait for reconnection with a few bounded checks, then re-enumerate host browsers, read a real work DOM and test screenshots separately. Static registration is not live capability proof. Save progress and hand off any necessary restart; keep browser processes running.

## DOM works but screenshot times out

Record the failing API, host/extension versions and independent DOM/screenshot results for the same public page. Check visible capture surface, tab authorization and connection. Use at most two purposeful diagnostic rechecks, retaining persistent errors. Continue independent DOM-only work. Healthy static bridge checks lead to screenshot diagnostics rather than automatic runtime replacement.

## Page/player loading

Refresh live DOM, click play and wait roughly 3–10 seconds with few progress checks. Inspect other same-site players; pause task-owned playback first and coordinate user-owned players without closing them. Then inspect network or visible blocking evidence. Placeholder images and `00:00/00:00` do not establish a cause. Disable task autoplay and record the end state before switching. Classify Bilibili 412 as page-access restriction; do not initiate buvid/playurl acquisition.

## Failure and recovery

Preserve diagnostics for signature, hash, compatibility or path failures. Inspect existing receipts before rerunning. A failed repair with recorded changes supports `Rollback` using the same receipt; later user edits block automatic restoration. Private backups remain in `.workbuddy/bridge-backups/` and are excluded from delivery. Inspect the original process before manually resolving an interrupted lock. After two evidence-based repairs fail, hand off consolidated diagnostics and continue independent tasks through healthy browsers.


Error routing: `provider invocation timed out` with working DOM enters screenshot diagnostics; `Current display surface not available for capture` enters visible-surface checks; extension “WorkBuddy is not running” enters connection/native-messaging checks. Check without an observed extension ID reports null matching. Plan/Repair requires explicitly selected browsers.
