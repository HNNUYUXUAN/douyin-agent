# Visual assistance

Prefer live DOM. Use configured Agent Plan for screenshot interpretation without requiring a host-model switch.

`inspect --session SID --image PAGE_PNG_OR_JPEG --snapshot SNAPSHOT_ID --goal QUESTION`

Use the [session](browse.md) command prefix and an explicitly approved allowance. This paid call consumes one request and one image, with a 2048-token output ceiling. Capture only the necessary task-page area, excluding account/private tabs. Results contain observation, candidates, uncertainty and snapshot/hash/dimensions. The host verifies current state and candidates before acting; model output grants no permissions. The input file is preserved. The host records path/hash ownership for temporary captures and cleans them individually at task end. Failed or malformed responses are not automatically retried; submitted usage remains in the ledger.

On missing Key, exhausted limits, pending calls or missing capture capability, defer affected work and continue independent DOM steps. Collect user intervention only when available routes cannot complete the work.

Models may produce normalized or out-of-bounds coordinates. Candidates are advisory: resolve semantic labels and verify the current snapshot, actual dimensions and visible target before acting. A single outer JSON code fence can be removed locally while retaining the original response, without resubmitting the request.
