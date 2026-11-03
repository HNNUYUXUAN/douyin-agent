# Short-video case: recursion through a parking queue

[中文](short.zh.md) · [Bilingual evidence JSON](short.json)

Source: [递归到底是什么？3分钟看懂递归](https://www.douyin.com/video/7683763028419956019), by 猫小申. Work ID: `7683763028419956019`.

This case follows a 2-minute-54-second animated explanation through fresh transcription and distributed frame sampling, producing reviewed text that remains readable after media cleanup.

| This run | Result |
|---|---|
| Media duration | 174.375 seconds |
| Visual input | 68 sampled frames |
| Audio coverage | Fresh full-file transcription; 41 native speech segments |
| Actual submissions | 15 requests, 68 images, 174.375 audio seconds |
| Request stages | One ASR, 11 vision, two hierarchical summaries, one report |
| Understanding model | doubao-seed-2.1-pro |
| Final state | completed; registered media removed; post-cleanup text validation passed |

## What remains

The corrected result explains the queue analogy: asking the preceding car reduces the problem, the front supplies a definite answer, and successive returns complete each waiting calculation. Early visible labels support character ordering. The final frame shows cars without labels, so it is not used alone to establish each character’s identity.

## What review prevented

- **Coverage confusion:** the first vision request contains eight frames, not the whole task. The run sampled and submitted 68 frames across the video.
- **Timing confusion:** `f00046` is a global frame position at **103.669 seconds**, and `f00053` at **125.367 seconds**. These are image positions, not native server speech times or frame-duration intervals.
- **Text misquotation:** the original speech bubble in `f00032` at **74.738 seconds** reads “我第一啊”; the host corrected an imprecise rendering.
- **Unsupported truncation claims:** missing ASR words remain transcription uncertainty, rather than proof that the acquired video's audio was truncated.

The JSON retains six host-reviewed frame IDs, global times, full SHA256 values and bilingual observations. It does not publish video, full transcription or private request records.

## Validation boundary

The host checked six key original frames and ASR response text, without every-frame inspection or full manual listening. The animation explains a concept rather than providing a compilable program, and this review did not compile or execute code. Registered media and browser-download copies were removed; the remaining results passed validation after cleanup. Submitted quantities do not substitute for settled billing or promise fixed costs or universal acquisition success.
