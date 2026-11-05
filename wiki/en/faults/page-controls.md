---
{
  "type": "Runbook",
  "title": "Page initialization, input and scrolling recovery",
  "description": "Page initialization, input and scrolling recovery",
  "tags": [
    "page-controls",
    "fault",
    "troubleshooting",
    "故障"
  ],
  "status": "stable",
  "generated": {
    "by": "douyin-agent/2.5.1",
    "at": "2026-11-05T09:44:27.533063+00:00"
  },
  "sources": [
    {
      "resource": "../../shared/acceptance/field-v251.md"
    },
    {
      "resource": "https://github.com/GoogleCloudPlatform/knowledge-catalog/blob/62432a095456147ee71e70ac6e4dc0d2dea3ac30/okf/SPEC.md"
    }
  ],
  "applicability": {
    "skill": "2.5.1 candidate",
    "host": "Windows x64; recheck current host capabilities"
  },
  "verification_scope": "Candidate implementation; fixture, local and recipient results are recorded separately."
}
---

# Page initialization, input and scrolling recovery

Trigger: empty DOM/transient error title, applied:true with empty input, cua_scroll timeout or blank/misaligned rendering. Observed on WorkBuddy 5.9.3/extension 0.2.8; recheck other versions. Focus, first paint and host-channel failures are possible, not proven framework causes.
Preconditions: record browser/tab IDs, exact failing interface and page state. Use Chrome/Edge and never experiment in a login-handoff tab.
Procedure:
1. Initial blank: wait 3–10 seconds and re-read DOM/title, at most two checks. Record actual 412/login-wall evidence separately; transient titles are not final access verdicts.
2. After typing, compare the real input value with the intended link. On mismatch reobserve, click the input, confirm focus, Ctrl+A and type once more. Read again before submission. Still mismatched: stop that site attempt. applied:true does not prove accepted text. Never read an unknown clipboard.
3. On scroll timeout stop repeating that interface. Try one PageDown/PageUp or visible anchor, then inspect DOM. If needed save input/progress and reload the work page once. Preserve user tabs and login handoffs.
4. For player placeholders, use the platform guide to click play, wait for initialization, check other task players and autoplay. Do not close user playback tabs or infer ad-blocker failure from placeholders.
Success: verify actual DOM, value, viewport and playback progress independently; capture success and playback completion are separate evidence.
Bounds: one input correction, two initialization checks, one alternate scroll and one work-page reload. No repeats without new evidence.
Stop/resume: healthy static bridge configuration does not call for runtime redeployment. Preserve state and follow [unknown faults](unknown.md).


Current runtime procedure / 当前运行流程：[v2.5.1](../operations/runtime-host.md).
