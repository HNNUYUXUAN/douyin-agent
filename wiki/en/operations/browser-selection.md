---
{
  "type": "Runbook",
  "title": "User browser selection and conditional login tabs",
  "description": "User browser selection and conditional login tabs",
  "tags": [
    "browser",
    "chrome",
    "edge",
    "user_tabs",
    "login"
  ],
  "status": "stable",
  "generated": {
    "by": "douyin-agent/2.5.1",
    "at": "2026-11-05T09:57:06.630627+00:00"
  },
  "sources": [
    {
      "resource": "https://www.codebuddy.cn/docs/workbuddy/From-Beginner-to-Expert-Guide/Function-Description/Right-Sidebar"
    }
  ],
  "applicability": {
    "skill": "2.5.1 candidate",
    "host": "Windows x64; recheck current host capabilities"
  },
  "verification_scope": "Candidate implementation; fixture, local and recipient results are recorded separately."
}
---

# User browser selection and conditional login tabs


## Trigger and scope
All platform pages, including public pages, short-link verification and login. Use Chrome/Edge user extension connections. IAB is auxiliary for public parsers/documentation.
## Preconditions
Inventory connected instances: family, kind, connection, DOM, screenshot and file saving. WorkBuddy must expose user_tabs; store host_capabilities in v2 observations. Missing legacy evidence requires a live recheck, not a missing-plugin diagnosis. Never read cookies, credentials, user-data folders or disconnected profiles.
## Ordered procedure
1. An explicit browser ID wins. If unavailable, return connect_user_browser and read recovery; never silently substitute another instance.
   With working connection/DOM but blocked platform access, return platform_blocked and retain that instance. Follow the page/login branch rather than reinstall a healthy bridge.
2. Otherwise live-check the last binding, then a logged-in instance that accesses the work. Choose once among equivalent instances. IAB is never a platform candidate.
3. Without platform observations, probe_platform first. Connection or an avatar alone does not establish login. Record logged_in/logged_out/unknown separately from access; conflicting evidence stays unknown pending account-control verification.
4. logged_in: reuse/create the work tab only (login_action=not_needed). logged_out/unknown: reserve/reuse login and work tabs in the same Profile (reserve_login_tab). Hand off the login tab without navigating/closing it. A supplied public link may enter parser acquisition without login.
5. After confirmed login, release only a task-created login tab with completed handoff and no remaining purpose. Preserve pre-existing user tabs. Record ownership first; a suggested obsolete-tab ID is not deletion authorization.
6. Recheck and reuse the work tab later. If an IAB parser redirects to a platform, verify there through the selected user browser.
## Success and bounds
Verify access, login, playback, capture and saving independently. Reuse selections. On failure read [recovery](browser-recovery.md) completely instead of repeatedly switching browsers.
## Record and resume
`onboard --check --host workbuddy --browser-id OPAQUE_ID --observed CURRENT_JSON` uses current observations; --record persists v1/v2 receipts. Local output remains advice: the host performs navigation and may bypass the workflow, which this script cannot intercept.
