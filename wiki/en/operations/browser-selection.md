---
{
  "type": "Runbook",
  "title": "Cross-browser selection and two-tab collaboration",
  "description": "Cross-browser selection and two-tab collaboration — douyin-agent operational knowledge",
  "tags": [
    "chrome",
    "edge",
    "login",
    "登录",
    "双标签",
    "browser"
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

# Cross-browser selection and two-tab collaboration

## Observe live capabilities

Inventory all host-connected Chrome/Edge instances and visible tabs. Inspect existing selected-platform tabs first; open a public platform page in candidate instances when needed. Limit inspection to selected platforms. Record connection, DOM, screenshot and file-save independently. Do not inspect browser user-data directories, cookies or unconnected profiles.

Use visible login/account controls and page state to classify `logged_in|logged_out|unknown`; record access separately as `passed|blocked|unverified`. An avatar or playback alone does not prove login. Login state is a time-specific observation.

## Choose and reuse

Honor explicit user choice. Otherwise recheck the previous binding, then prefer logged-in instances able to access the work. Use a sole candidate; ask once among equivalent candidates and save the choice. Without a logged-in instance, public-page access and parser acquisition may still work.

`onboard --record` v2 stores opaque browser IDs, kind, four capabilities, per-platform login/access and tab bindings without account names. Returned `browser_choices` are historical suggestions requiring live recheck. Reobserve changed connection IDs and stale tabs.

## First-use tabs

For the selected platform's first use, create/reuse login tab A and work tab B in the same instance/Profile. A remains with the user for login, CAPTCHA or confirmation of existing login. B handles browsing and public link collection. Do not navigate A while the user signs in.

Save `first_use_complete`, `browser_id`, `login_tab`, `work_tab` and evidence after actual setup. Later recheck and reuse the work tab. Close only unneeded agent-created probe tabs; retain user tabs and the login tab.

Field evidence covers WorkBuddy 5.9.3 / extension 0.2.8: extension-session reuse worked and the built-in instance had login persistence problems. Detect current capabilities rather than generalizing this result to every built-in browser version.


[桥接与截图恢复 / Bridge recovery](browser-recovery.md) · [v2 receipt example](../../../docs/agent/examples/onboard-v2.json)


## Login handoff / 登录交接

When login needs user takeover, use the actual host keep/handoff capability to retain the login tab. Do not navigate or close it while waiting.
