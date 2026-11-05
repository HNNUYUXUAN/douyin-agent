---
{
  "type": "Runbook",
  "title": "Recovery, cleanup and migration (2)",
  "description": "Recovery, cleanup and migration (2) — douyin-agent operational knowledge",
  "tags": [
    "douyin-agent",
    "en",
    "operations",
    "recovery-part2"
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

# Recovery, cleanup and migration (2)

## Procedure

Start with read-only `status`, `doctor` or `onboard --check`. Determine whether the issue concerns environment, browser, media acquisition, a service request, review or cleanup. See the detailed [recovery contract](../../shared/recovery-protocol.md).

| State/symptom | Next action |
|---|---|
| Browser disconnected/profile changed | Rediscover and bind tabs through onboarding; verify account/access without resubmitting in-flight work |
| Restricted acquisition/unknown completeness | Record why and stop this work's paid understanding; local input may help, while independent work continues |
| `review_ready` | Inspect original frames, write review matching the current report hash, then finalize |
| `cleanup_pending` | Check the exact path, hash, acquisition proof and file lock; resolve then retry finalize without widening deletion scope |
| Completed with media removed | Read durable text; reacquire and preview for new visual questions |
| Unresolved paid request | Preserve the original ledger/reservation and reconcile that request first; do not resubmit directly |

### Unresolved requests: collect read-only evidence first

This version has **no `reconcile` command**. For an unfinished job, `run/resume` stops when any pending record belongs to that job. It neither skips nor resubmits that job automatically, and the current batch may stop. `resume` is not a general retry button after a timeout.

Commands use `PYTHON SKILL/scripts/da.py --workspace WORKSPACE COMMAND`. Diagnose with `status` (and `doctor` or `onboard --check` when needed); do not use `run/resume` or `cleanup` as read-only diagnostics.

1. Find the target job's absolute path and `state.status` in `status.jobs`; collect filenames from `pending` and note `locked`. Read the target `metadata.json` and confirm `source.id` and `media_identity` identify the original work.
2. Read the relevant `cache/<cache_id>.pending.json`. Collect `cache_id`, `job`, `plan`, `at`, `status`, `error_type` when present, `charge`, and `identity.stage`, model and processing-version fields when present. `job` may be a directory name or an `out/jobs/...` relative path; map it to the actual target. Do not infer ownership from recency alone.
3. Match the submission in the `requests.json` array by **plan + job + cache_id**, retaining all matching records. Collect `status`, `charge.audio_seconds/images/requests`, and any `request_id`, `usage`, `billing` and `error_type`. A missing request ID stays unknown. Read `id`, target `jobs`, `new_usage`, model/options in `out/plans/<plan>.json` to establish the approved scope; do not edit the plan ID or budget.
4. If `cache/<cache_id>.response.json` exists, inspect its evidence for that original request without changing it. Collect `id`/`log_id`, `status`, `incomplete_details.reason`, `error` and `usage` when present. Interrupted transport may be stored as `{status:transport_interrupted,response:...,partial_text:...}`: distinguish the outer interruption from the inner response status. `partial_text` is not a complete result. An absent response file does not establish that no charge occurred.
5. When a platform lookup is available for the original request ID, verify that request's terminal state and complete result. Put the identifiers, evidence sources, lookup time and remaining unknowns in a separate workspace MD/JSON investigation record for maintainer assistance. Do not send Keys, cookies, authorization headers, complete private responses or signed media URLs to chat or public issues.

**Without a verifiable terminal state and complete successful result for the original request, preserve the reservation and stop this job.** `incomplete/length` is a known truncated terminal state, not a complete success. Never assemble partial output into a successful cache, delete pending records, rewrite ledger state/budgets or create another job for the same work to unlock execution. Even with platform evidence, this version has no automatic import/reconciliation interface. Maintainer assistance needs its own record linking the original request and platform evidence; this guide does not instruct manual runtime-state edits.

Independent works may continue under a separate preview within valid authorization; exclude the blocked job from that batch. Use `resume --plan PLAN --approve ID` only after confirming no pending record belongs to the target job, existing inputs/metadata still match the original plan, and usage/authorization have not expanded. It reuses complete cached results and continues unfinished steps, which may still incur new calls within the preview. Expanded scope needs a new preview, not edits to the old plan to bypass checks.

For completed jobs whose media were cleaned, directly read `analysis.md`, `understanding.json`, `segments.json` and other durable text, optionally checking with `validate --job JOB`. Reading a summary does not require resubmitting its original request. New visual questions require reacquisition and preview. Preserve returned `usage` separately from settled platform billing.

Failed/interrupted media remain for 24 hours after the first failure; inspection/recovery does not renew that deadline. `cleanup --expired` runs at task entry or when explicitly invoked by the host, with no background scheduler. Active or unknown process locks protect media. Check PID and process creation identity; do not simply delete a lock to proceed.

For historical upgrades, run `migrate --dry-run` and inspect paths, request count, audio seconds, image count and pending records. Then use `migrate --apply` with no active worker. Keep code/text backups outside skill discovery. Preserve user originals; media are not backed up and cannot be rolled back. Validate each text result before cleanup, with identical ledger and pending hashes before/after migration.

Cleanup deletes individual files with proven ownership only. External downloads require exact absolute paths, acquisition records and SHA256. Preserve/report unknown files; never clear Downloads or browser caches. Cleanup does not release unresolved-request protection.
