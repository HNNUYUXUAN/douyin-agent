---
{
  "type": "Runbook",
  "title": "First use and recovery",
  "description": "First use and recovery — douyin-agent operational knowledge",
  "tags": [
    "douyin-agent",
    "en",
    "bootstrap",
    "first-run"
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

# First use and recovery

Reuse existing configuration and fill only missing/failed prerequisites. Record each check separately as passed / blocked / unverified.

1. Discover existing Git Bash → PowerShell 7 → Windows PowerShell 5.1 and record actual executable/version. Check architecture, storage, short writable workspace and host session directory separately.
2. Obtain one release commit as an ordinary source directory. Reuse Conda, Python 3.12 and FFmpeg/FFprobe; prepare missing dependencies using the guide.
3. New WorkBuddy installations use the current user's `.workbuddy/skills/douyin-agent`; preserve existing receipt paths. Verify actual skill invocation.
4. Discover existing search skills, host-native search and file-saving capabilities. Download tools save parser results.
5. After the user selects a platform, inventory connected Chrome/Edge instances and visible platform tabs/login state. Complete first-use two-tab setup for that platform; onboard others when first selected.
6. Reuse configured Agent Plan. Otherwise open official setup and let the user enter the Key locally. Setup itself makes no paid request.
7. Start only after explicit user instruction and mode/scope selection. Preview a concrete sample and execute, review, clean and record within existing authorization.

The user handles login, CAPTCHA, purchases and credentials. Public links/parsers can remain usable while logged out. Recheck current capabilities rather than trusting historical passed records.


[依赖 / Dependencies](dependencies.md) · [WorkBuddy](workbuddy.md) · [浏览器 / Browsers](../operations/browser-selection.md) · [配置回执 / Receipts](../operations/onboarding.md) · [浏览 / Browse](../operations/browse.md)

[File-save preflight and same-round standard transport](../operations/parser-sites.md). Existing curl can save public parser-result files; probe it separately from browser download APIs.
