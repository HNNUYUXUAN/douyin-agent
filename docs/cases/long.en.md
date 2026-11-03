# Long-video case: explaining recursion

[中文](long.zh.md) · [Bilingual evidence JSON](long.json)

Source: [8分钟搞懂“编程的鬼打墙”——递归](https://www.douyin.com/video/7493866919565610291), by 林粒粒呀. Work ID: `7493866919565610291`.

This case follows an 8-minute-26-second video through completeness checks, full-audio transcription, sampled vision, evidence review and media cleanup, leaving traceable text results.

| This run | Result |
|---|---|
| Media duration | 506.21678 seconds |
| Visual input | 102 sampled frames |
| Audio coverage | 0–300 and 300–506.21678 seconds; 94 native speech segments |
| Actual submissions | 22 requests, 102 images, 506.21678 audio seconds |
| Understanding model | doubao-seed-2.1-pro |
| Final state | completed; registered media removed; text validation passed |

## What remains

The corrected result explains self-calls, reachable termination and factorial call/return chains. It distinguishes the author's teaching claims, visible formulas and static boundary inferences. For example, a slide and the complete demonstration use different base-case conditions. The demonstration's handling of negative values does not establish a mathematical definition of negative factorials.

## What review corrected

The model report confused global frame positions with native ASR times: it subtracted the second audio chunk's 300-second offset from a frame position and presented the result as speech timing. The host removed that inference using frame records and the server's original timing fields.

- Frame `f00065` is at **308.084 seconds globally**; that locates a sampled image only.
- A speech segment on the same topic has native start/end **1,640–8,720 milliseconds** and a **300-second** chunk offset, yielding a global speech range of **301.64–308.72 seconds**.
- The base-case difference in `f00072`/`f00080` and the displayed return result in `f00097` remain visual observations, not verbatim speech evidence.

The JSON retains evidence identifiers, full SHA256 values and bilingual observations. Original video, full transcription and complete teaching code are not published.

## Validation boundary

The host reviewed four critical code/formula frames, acquisition head/tail frames and native speech timing. This was not every-frame inspection, full manual audio listening or code compilation/execution. Completeness checks are not a byte-for-byte comparison with the author's master file. Submitted quantities describe this run; settled billing is unverified, and neither fixed costs nor universal acquisition are promised.
