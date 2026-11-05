---
{
  "type": "Runbook",
  "title": "Codex host setup",
  "description": "Codex host setup",
  "tags": [
    "codex",
    "host",
    "setup"
  ],
  "status": "stable",
  "generated": {
    "by": "douyin-agent/2.5.1",
    "at": "2026-11-05T09:44:27.533063+00:00"
  },
  "sources": [
    {
      "resource": "https://learn.chatgpt.com/docs/chrome-extension"
    }
  ],
  "applicability": {
    "skill": "2.5.1 candidate",
    "host": "Windows x64; recheck current host capabilities"
  },
  "verification_scope": "Candidate implementation; fixture, local and recipient results are recorded separately."
}
---

# Codex host setup


## Trigger and prerequisites
First setup or a failed connection. Read the setup pack and use actual host tools, never another host's command names.
## Procedure
New user skill location: `.codex/skills/douyin-agent`; reuse a matching existing receipt. Record runtime workspace separately from the host conversation directory. Verify discovery through host skill listing/actual invocation; leave fresh-chat invocation pending when untested.
Platform pages use user Chrome/Edge extension instances only; IAB is auxiliary for public parsers/docs. Use actual Codex extension/user-tab evidence; WorkBuddy field names are not required.
Read a public page DOM and capture it; record connection, DOM, screenshot and file saving separately. Setup need not download works: file saving may remain unverified until the explicit start. Do not visit all platform login pages.
## Success and bounds
Static registration does not establish connectivity. Mark DOM and screenshot passed only with live evidence. Route discovery/connection faults through the fault index; do not repeatedly install. Users handle login and credentials locally.
## Stop and resume
Use the browser recovery branch on connection failure, preserving installed resources. After browser checks, enter Key setup and wait if missing.
