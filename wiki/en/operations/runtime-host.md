---
{
  "type": "Runbook",
  "title": "Browser, screenshot and file receipts",
  "description": "Browser, screenshot and file receipts",
  "tags": [
    "douyin-agent",
    "en",
    "runtime-host",
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

# Browser, screenshot and file receipts

Trigger: no browser, disconnected extension, screenshot timeout, unavailable export, stale nodes or save clicks without a file. Applies to the v2.5.1 candidate. Inspect live host and page evidence; never read cookies, credentials, Chrome Preferences or private temporary folders.

1. Explicit Chrome/Edge preference also applies to parsers. Distinguish a stopped process, disconnected extension, unauthorized tab and failed page. Use `powershell.exe -NoProfile -File SKILL/scripts/browser-ready.ps1 -Browser Chrome -Mode Check`. Within installation authorization, `-Mode Launch` starts that selected installed browser; then perform bounded host checks. Process presence does not prove extension connection. Do not reinstall a healthy bridge or stop user browsers.
2. Git Bash example: `powershell.exe -NoProfile -File 'C:/skill/scripts/workbuddy-bridge.ps1' -Mode Check -Browser Chrome,Edge`. PS7 example: `& 'C:\skill\scripts\workbuddy-bridge.ps1' -Mode Check -Browser @('Chrome','Edge')`. Substitute actual paths. Both normalize to strict Chrome/Edge values.
3. Logged-in: reuse/create a work tab. Logged-out/unknown: preserve login and work tabs in the same Profile, leaving the login tab to the user. Public links can enter parser acquisition while waiting. Page reading and playback are distinct capabilities.
4. Verify and focus the target before capture. Record inline screenshot and file export separately. If export is unavailable, retain that limitation and use DOM or an explicit file handoff, not private-cache searches. Diagnose once through the screenshot manual.
5. Prefer semantic controls. Observe after page changes; relocate once after a stale node. Read actual input value after writing and before submission. Allow initialization before classifying an empty DOM. Switch failed scrolling to keyboard navigation and observe again.
6. Before save: `PYTHON SKILL/scripts/save_watch.py --workspace WORKSPACE before`. After click: `... after --id WATCH_ID`. Missing files are not_observed; several candidates are ambiguous, neither proves a host-wide failure. Only after host confirmation of task creation use `--expected-name FILE --confirm-created-by-task`. The receipt records path, size and SHA256; decode, identity, duration/image order still require verification. Recent files alone do not establish ownership.

Success requires current per-capability evidence and an actual verified file for acquisition. Limit connection/focus checks and stale relocation; do not repeat a denied link through proxies. Save the stage, instance, error and resume position on handoff. Missing Key still waits for local entry; ordinary setup ends after configuration.
