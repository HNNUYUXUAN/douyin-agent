# Fault routing index

Match a code/symptom, then read the entire matched manual before acting. Historical IDs work with knowledge.py route.

| Code / 编号 | Symptom / scope | Manual |
|---|---|---|
| install | Installation, terminal and source faults | [read](install.md) |
| conda | Conda verification, wait and partial installation | [read](conda.md) |
| page-controls | Page initialization, input and scrolling recovery | [read](page-controls.md) |
| acquisition | Parser results, empty results and file acquisition faults | [read](acquisition.md) |
| records | Observation, knowledge and session receipt faults | [read](records.md) |
| media | Media identity, sampling and cleanup faults | [read](media.md) |
| unknown | Bounded diagnosis for faults outside the manuals | [read](unknown.md) |
| browser.* / F241-4 / O-1,O-3 | Chrome/Edge, login | [read](../operations/browser-selection.md) |
| browser.extension_offline / browser.screenshot_timeout | Bridge / capture | [read](../operations/browser-recovery.md) |
| key.missing / O-4 | Key | [read](../bootstrap/key.md) |
| O-5 | setup | [read](../bootstrap/first-run.md) |

## Exact routing and stop

`PYTHON SKILL/scripts/knowledge.py --workspace WORKSPACE route --code browser.scroll_timeout --language en`

See [42 original issue mappings](../../shared/acceptance/field-v251.md). Only unmatched faults use unknown: one official-search round, three primary sources and two distinct diagnostics, without repeating unchanged failures or opening another round.

Latest feedback / 最新一轮：F251R-I-1～I-8、F251R-R-1～R-14，见 [coverage](../../shared/acceptance/runfix-v251.md)。
