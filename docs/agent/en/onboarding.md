# First use and configuration recovery

[中文](../zh-CN/onboarding.md) · [Index](../index.json)

## Applicable intent

Prepare first use, or restore browser and Agent Plan configuration after invalidation or changes.

## Prerequisites

An installation and locatable workspace exist, and the host can guide browser connection. The user still completes login, purchase and local Key entry.

## Minimum inputs

Actual Python/skill/workspace paths, the selected browser and observations to record. Real-service validation additionally needs a concrete sample and authorization covering its usage.

## Procedure

Bring connection, login, subscription and local Key entry into one guided session, then reuse valid configuration. The host checks capabilities and opens pages; an installer cannot prove browser connectivity. Skip steps already supported by valid evidence.

### Check before guiding

Run `PYTHON SKILL/scripts/da.py --workspace WORKSPACE onboard --check`. It is read-only: no record writes, browser opening or cloud calls. Follow the returned next steps. `doctor` checks the local environment and `status` inspects jobs; neither proves subscription availability.

The host separately verifies browser connection, selected profile, Douyin access, any required login, local Agent Plan Key presence and actual service validation. One successful check does not imply another. Use `onboard --record FILE` to save non-sensitive host observations to workspace `onboarding.json` and update local `agent-context.json`. These support future routing and must not contain credentials or private page contents.

### Browser

Prefer a connected Chrome on the tested device. If the user selects Edge, verify that browser's own profile and permissions. Follow the [official connection guide](https://learn.chatgpt.com/docs/chrome-extension): desktop Settings → Computer Use installs/manages the corresponding extension, and `@Chrome` or `@Edge` selects it in chat. Follow the actual host UI if labels change.

Once connected, open [Douyin](https://www.douyin.com/) in that same profile. The user handles login, CAPTCHA and permission prompts where required. Record access as passed only after the host reads the actual page title or target work. Never request exported cookies. Without a connection, provide the official guide first, let the user connect, then open the remaining pages; do not claim inaccessible tabs were opened.

### Agent Plan

Open official pages for the steps still needed:

| Page | User action |
|---|---|
| [Subscription page](https://www.volcengine.com/activity/agentplan) | Sign in and purchase the chosen plan, or reuse an existing subscription |
| [Agent Plan console](https://ark.volcengine.com/region:cn-beijing/openManagement?LLM=%7B%7D&advancedActiveKey=agentPlan) | Obtain the dedicated Agent Plan Key and check actual entitlements |
| [Official quickstart](https://docs.volcengine.com/docs/ark/agent-plan-personal-get-started?lang=zh) | Check product configuration guidance |

The host prepares and opens the workspace `.env`; the user enters `VOLC_AGENT_API_KEY` locally. Never request a Key in chat, capture it in screenshots or echo it. Preserve the existing file. Process environment variables override workspace `.env`. Agent Plan uses a dedicated Key, distinct from ordinary Ark/Coding Plan Keys. The scripts already select Plan endpoints; the user need not change Codex's main model configuration.

The user completes purchase, payment, login and verification. Current console terms determine prices, limits and entitlements; historical Small-plan evidence is not a guarantee for every account today. Do not automatically enable renewal or overage billing.

### Validate and reuse

After Key entry, perform local checks first. For a real-service test, use a specific acquired work and follow the [workflow](workflow.md): show usage before running within user authorization. Record errors using actual HTTP/protocol evidence; leave unknown states unknown. Save completed and outstanding steps. Recheck only missing, changed or invalid parts next time, and reverify after changing browser profiles.

### Host-check receipt

This is a format example, not test evidence: replace every observation. `status` allows `passed`, `blocked`, `unverified` and `not_applicable`; use the actual UTC `observed_at`. `evidence` is a verifiable public URL or workspace-relative JSON evidence path. Record only `browser_connection`, `douyin_access` and `agent_plan_call`; omit account and browser-profile names.

```json
{
  "schema_version": 1,
  "checks": {
    "browser_connection": {
      "status": "passed",
      "observed_at": "2026-11-03T00:00:00Z",
      "evidence": "https://www.douyin.com/"
    },
    "douyin_access": {
      "status": "unverified",
      "observed_at": "2026-11-03T00:00:00Z",
      "evidence": "qa/onboarding-check.json"
    },
    "agent_plan_call": {
      "status": "unverified",
      "observed_at": "2026-11-03T00:00:00Z",
      "evidence": "qa/onboarding-check.json"
    }
  }
}
```

`onboard --record FILE` records host observations. A later `onboard --check` returns local checks and historical observations; an earlier pass does not prove current permissions or service availability.

## Expected outputs and success evidence

The read-only check returns local state and historical observations; recording writes non-sensitive onboarding.json and agent-context.json. Every pass has actual evidence, while missing steps remain pending. Historical state is not live availability proof.

## Stop or recovery conditions

Pause only actions depending on incomplete connection, login, verification or Key entry; local checks may continue. Follow [recovery](recovery.md) for real-request errors while retaining reservations.

## Next links

Once configured, read [acquisition](acquisition.md); with media already acquired, proceed to the [workflow](workflow.md).
