---
{
  "type": "Runbook",
  "title": "Local Agent Plan Key setup",
  "description": "Local Agent Plan Key setup",
  "tags": [
    "key",
    "setup",
    "waiting",
    "local_key"
  ],
  "status": "stable",
  "generated": {
    "by": "douyin-agent/2.5.1",
    "at": "2026-11-05T09:44:27.533063+00:00"
  },
  "sources": [
    {
      "resource": "https://www.volcengine.com/activity/agentplan"
    }
  ],
  "applicability": {
    "skill": "2.5.1 candidate",
    "host": "Windows x64; recheck current host capabilities"
  },
  "verification_scope": "Candidate implementation; fixture, local and recipient results are recorded separately."
}
---

# Local Agent Plan Key setup


## Trigger and scope
Windows first setup, after dependencies, installation and browser connection. Reuse an existing Key without repeated purchase/configuration.
## Preconditions
Read only key_present from doctor/onboard. Process environment overrides workspace .env. Presence does not prove subscription or API success.
## Procedure
If missing, open the [official page](https://www.volcengine.com/activity/agentplan) and [console](https://ark.volcengine.com/region:cn-beijing/openManagement?LLM=%7B%7D&advancedActiveKey=agentPlan), showing the actual WORKSPACE/.env path. The user logs in, purchases if needed and fills VOLC_AGENT_API_KEY locally. Never request it in chat, echo it, capture it or dump the environment.
Use `onboard --record CURRENT_JSON` to save non-sensitive current observations and progress; the key phase returns waiting_for=local_key. End execution and wait for local entry. No skip option or subsequent acquisition, sessions or paid calls.
## Verification and bounds
After the user confirms entry, check locally once; remain waiting if still absent. Respect process-env precedence without displaying values. This step makes no API request.
## Completion and resume
At finish_setup, report local configuration completed and real service unverified. Reuse the installation on resume; works require a later explicit start. Use the dedicated Agent Plan Key, not another product's Key.
