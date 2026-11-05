---
{
  "type": "Runbook",
  "title": "Request recovery, cleanup and migration",
  "description": "Request recovery, cleanup and migration",
  "tags": [
    "douyin-agent",
    "en",
    "recovery",
    "v251-runtime"
  ],
  "status": "active",
  "generated": {
    "by": "douyin-agent/2.5.1",
    "at": "2026-11-05T15:01:35.569439+00:00"
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

# Request recovery, cleanup and migration

Trigger: transport timeout, interrupted SSE, truncation, unresolved reservation or blocked recovery. Applies to the v2.5.1 candidate. Confirm the actual workspace, original plan/job/cache_id and process lock; retain the original records.

Prefix every command with `PYTHON SKILL/scripts/da.py --workspace WORKSPACE`, substituting receipt paths:
```text
requests status
requests status --cache-id CACHE_ID
requests reconcile --cache-id CACHE_ID
requests retry --cache-id CACHE_ID
requests retry --cache-id CACHE_ID --approve RECOVERY_PREVIEW_ID
resume --plan WORKSPACE/out/plans/ORIGINAL_PLAN.json --approve ORIGINAL_PLAN_ID
requests abandon --cache-id CACHE_ID
```
Status is read-only. Mutations hold the workspace lock. Run one pipeline and wait through its existing process handle. Local progress JSON every 15 seconds is separate from the final result; repeated shells or screenshot polling are unnecessary.

Reconcile checks a saved complete successful result, or reliable correlated evidence supplied as `--evidence WORKSPACE_RELATIVE.json`. A known platform response ID, completed state and complete text must match. A local cache_id is not a platform ID. No lookup API is guessed; store:false remains the default. Complete cache writes interrupted before the ledger transition can be reconciled too. Unknown evidence retains the original reservation.

Retry creates an additional usage preview. Approve its id only within applicable authorization, then resume the original plan. Development uses standing maintenance authorization. Each logical unresolved call permits one independent attempt, linked to the original and counted separately. Successful ASR, vision and downloads are reused. Original unknown/pending records and charges remain. A second unknown attempt requires reconciliation or abandonment; never delete pending, edit old budgets or switch jobs to bypass it.

Abandon saves a failure summary and recovery history and removes only hash-verified task-owned media. A successful report is unnecessary. User imports, unknown files, ledger and unknown terminal states remain. An unresolved work blocks its own effective attempt chain; independent works continue. Authentication, quota and model configuration errors pause related cloud calls until explicitly addressed.

Default connect timeout is 30 seconds and idle read timeout 300 seconds. Override locally with VOLC_AGENT_CONNECT_TIMEOUT / VOLC_AGENT_READ_TIMEOUT (1–1800). These are not a whole-request wall-clock limit and do not change content cache identity. Vision/merge/report output limits are 4096/4096/8192 and enter previews and cache identities. Truncated output never becomes a complete cache.

Diagnostics cover submission, response headers, first event, first text and completion, with actual model, request/response IDs, usage, error stage and elapsed time. Missing evidence remains unknown; missing headers/files do not establish that the server did nothing. ASR covers all audio with existing protocol pacing; upload and recognition waiting are measured separately, without unsupported acceleration.

Success requires review_ready, host review against real frames/audio, a review matching the report hash and finalize. Durable text remains reusable. Failed media retain the existing 24-hour expiry, or may be cleaned on explicit abandonment; neither changes reservations. Migration still requires dry-run, then apply without an active worker; preserve originals and accounting.
