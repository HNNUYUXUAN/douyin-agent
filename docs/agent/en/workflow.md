# Understand a work and deliver results

[中文](../zh-CN/workflow.md) · [Index](../index.json)

## Applicable intent

Preview, understand, review and deliver text for acquired single or batch works; also reuse completed results.

## Prerequisites

Workspace/runtime are configured, and actual media plus acquisition receipts are available for new work. Paid processing requires passed integrity and valid usage authorization.

## Minimum inputs

The understanding question and actual JOB directories or a batch jobs list. Execution uses PLAN and ID produced by this preview. Follow-up questions about completed text need only the existing result.

## Procedure

Read local `agent-context.json` when present and resolve actual Python, skill and workspace paths; use [onboarding](onboarding.md) when needed. Users may provide links, share text, local media or ask the host to find a topic on Douyin. Site search uses the connected browser; the CLI has no Douyin keyword-search command.

All commands use `PYTHON SKILL/scripts/da.py --workspace WORKSPACE COMMAND`. `JOB` is the returned job directory; `PLAN` and `ID` come from the current preview. Never reuse example values from an unrelated job.

`ID` is the `id` field of the current preview JSON. `PLAN` is the absolute path to its automatically saved plan file, `WORKSPACE/out/plans/ID.json` (replace WORKSPACE and ID with actual values). Preview prints JSON rather than a separate path; confirm that file exists before passing it to `--plan`.

1. Begin with `cleanup --expired`. Inspect `status`; prefer an existing task with the same source ID/media hash. Reuse completed text directly; new visual questions require acquisition again.
2. Open the actual work and verify its ID, author, title, complete caption, reliable duration or image count/order. Follow the [acquisition contract](../../../references/browser.md): direct download first; on blob/failure reuse successful free parsers, trying at most three distinct sources per round. Submit only public links, never account credentials.
3. Inspect real head/tail frames. Video receipts use `source_id`, `identity_verified`, `page_duration`, `head_tail_verified`, `method` and `host`; images use `expected_images` and `order_verified`. Only task-created downloads enter `owned_downloads`, each with absolute `path`, `sha256` and `created_by_task:true`. Never register a user original as a removable download. If individual image downloads fail, follow [ZIP acquisition](acquisition.md#when-individual-image-downloads-fail-acquire-a-zip) with `unpack_images.py --archive ABS --workspace ABS --output NEW_ABS_DIR --expected-images N`; output must be a new ASCII directory inside the workspace. Verify every image against the original page before confirming order. Do not pass a ZIP to adopt; list proven task-owned temporary ZIPs/extracted images in receipt `owned_artifacts` using absolute `path`, `sha256` and `created_by_task:true`. The acquisition guide provides copyable commands and a complete receipt example.
4. `adopt "SOURCE" --media "FILE1" "FILE2" --receipt "RECEIPT.json" --title "TITLE" --author "AUTHOR" --caption "CAPTION"` returns JOB and integrity results. A video job takes one file; image posts take ordered files. Local videos still need head/tail review; local images still need count/order receipts. Unknown source duration, wrong identity, truncation or decode failure blocks that work's cloud calls. Recheck using `integrity --job JOB`.
5. `preview --jobs JOB1 JOB2 --question "QUESTION"` produces usage; alternatively `--manifest FILE` reads a batch JSON with a `jobs` array. Present duration, images, coverage, model, caches and new-call upper bounds. Sampling adapts to duration; audio is fully covered while vision is sampled. Add important times in a JOB-local `extra-frames.json` seconds array and preview again.
6. After approval of this preview, or when valid continuing authorization covers it, use `run --plan PLAN --approve ID`. Added media/scope needs another preview. Downstream summaries reserve worst-case calls; cache hits incur no repeated call.
7. At `review_ready`, the host checks key numbers, formulas, code, conflicting captions and image order. Correct `analysis.md`, then write `review.json` with `status:sampled/verified`, the current `analysis_sha256`, and nonempty `checks` identifying evidence/time and actual observations. Do not claim review without inspecting original frames.
8. `finalize --job JOB` validates text before removing registered task media, including temporary ZIPs/extracted images in owned_artifacts; JSON manifests and receipts remain as text audit evidence. Both must succeed for `completed`; handle `cleanup_pending` through [recovery](recovery.md). Finish with `validate --job JOB` and deliver report/result-directory links.

Durable MD/JSON includes native subtitle timing, speech text, segment observations, evidence IDs/hashes, reports, validation and cleanup records. Without native timing, retain text with an explicit limitation; never invent timestamps. Reports must not embed local images or broken media links. User originals, runtime and private configuration remain.

A restricted public work does not fail the whole batch: record it and continue independent items. Follow recovery rules for authentication, quota and unresolved requests; creating another task ID must not bypass protection.

## Expected outputs and success evidence

Processing reaches review_ready; after host review, finalize validates text and cleans registered media before completed. Deliver analysis.md and evidence JSON, checking validation/cleanup results for the actual success scope.

## Stop or recovery conditions

Do not claim completion after integrity failures, plan changes, pending requests, authentication/quota errors, missing review or cleanup failure. Follow [recovery](recovery.md); expanded input/usage needs a new preview.

## Next links

Read the completed report; return to [acquisition](acquisition.md) for new visual questions or [recovery](recovery.md) for failures.
