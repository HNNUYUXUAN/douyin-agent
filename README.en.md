[简体中文](README.md) · English

![douyin-agent: Understand videos. Keep the knowledge.](docs/assets/hero-en.png)

# douyin-agent

A multi-platform video/image-post skill orchestrated by desktop agents including Codex and WorkBuddy. Supply a topic, shared URL or local media. Verify identity and completeness, use Volcengine Agent Plan for transcription and understanding, review evidence, retain Markdown/JSON and clean task-owned media.


Supports Douyin, YouTube, Xiaohongshu, TikTok and Bilibili videos/public image posts, including selected Bilibili parts. Media comes through free parser sites; accounts support browsing and identity checks.

## Install in natural language
```text
Install https://github.com/HNNUYUXUAN/douyin-agent
Read AGENTS.md and AGENT_INSTALL.md; for a new WorkBuddy device also read references/bootstrap/en/first-run.md.
Prefer existing Git Bash, then PowerShell 7, then Windows PowerShell 5.1.
Reuse Conda and prepare isolated Python 3.12, FFmpeg/FFprobe, browser and Agent Plan.
Open pages/local files for me when login, purchase, Key entry or system approval is needed.
```
[GitHub](https://github.com/HNNUYUXUAN/douyin-agent) · [GitCode](https://gitcode.com/yuxuan6426/douyin-agent) · [Zero-start](wiki/en/bootstrap/first-run.md)

Windows is the primary environment. Use the host's actual connected Chrome/Edge. Enter Keys locally and reuse valid configuration. Separate runtime workspace from skill location; new WorkBuddy installs default to user-level `.workbuddy/skills/douyin-agent`, subject to actual client discovery.

## Five complete workflow views

### 1. Install and onboard

```mermaid
flowchart TD
A["Repository URL"] --> B["Agent guides and existing install"]
B --> C["Git Bash then PS7 then PS5.1"]
C --> D["Conda Python 3.12 and FFmpeg"]
D --> E["Choose workspace and host skill directory"]
E --> F["Install and verify actual skill discovery"]
F --> G["Connect browser and open platform"]
G --> H["User login and local Agent Plan Key"]
H --> I["Read-only checks then concrete authorized sample"]
```

Read guides, prepare dependencies and verify browser/service separately. The user handles login, purchase and local Key entry.

### 2. From request to delivery

```mermaid
flowchart TD
A["Topic or URL or local media"] --> B["Resolve identity and read live state"]
B --> C{"Explicit browse session?"}
C -->|Yes| D["User chooses platform mode and finite limits"]
C -->|Direct analysis| E["Acquire media and verify completeness"]
D --> F["Muted sequential normal-speed playback"]
F --> G["Record observations and selected works"]
G --> E
E --> H["Concrete preview under applicable authorization"]
H --> I["Analyze then actual evidence review"]
I --> J["Finalize and deliver text results"]
```

Browse-only, selective and all-item analysis are explicit choices with no default spending mode.

### 3. Media acquisition

```mermaid
flowchart TD
A["Probe file-save capability"] --> B["Verified free parser"]
B --> C{"Verified file landed?"}
C -->|No| D["Discover parsers via existing skills then host search"]
D --> E["Configured Yuanbao then Bocha if needed"]
E --> F["Count every attempt; at most three sources"]
F --> G["User import or deferred item"]
C -->|Yes| H["Verify identity duration tracks decode head-tail"]
G -->|Imported| H
H --> I["Images: verify count and order; safe parser ZIP if needed"]
```

Parser success messages are not landed files. Count every attempt, defer blocked works and continue independent items.

### 4. System and data flow

```mermaid
flowchart TD
A["User"] --> B["Host agent and connected browser"]
B --> C["Local scripts and FFmpeg"]
C --> D["Complete audio chunks"]
C --> E["Adaptive sampled frames or ordered images"]
D --> F["Agent Plan ASR WebSocket"]
E --> G["Agent Plan Responses vision"]
F --> H["Native timestamps and observations"]
G --> H
H --> I["Layered report and host review"]
C --> J["Hash cache and request ledger"]
B --> K["DOM first; budgeted screenshot vision when needed"]
```

Audio is fully covered; video vision is sampled. Version ASR, vision and summarization separately and retain native timing and uncertainty.

### 5. Lifecycle and recovery

```mermaid
flowchart TD
A["Read live state cache and ledger"] --> B{"Unresolved request?"}
B -->|Yes| C["Retain reservation and reconcile"]
B -->|No| D["Reuse completed cache or continue remaining work"]
D --> E["review_ready"]
E --> F["Review original evidence and finalize"]
F --> G{"Text valid and cleanup successful?"}
G -->|Yes| H["completed: text remains readable"]
G -->|No| I["cleanup_pending and precise retry"]
I --> F
A --> J["Entry checks expired failed media after 24h"]
J --> K["Clean only owned inactive task files"]
```

No automatic paid resubmission. Viewing failed work does not renew its media expiry. No resident scheduler; doctor/status are read-only.

## Daily use and operation guides

After an explicit start, fill missing platform, mode, entry/topic, selection rules, time/item limits, image dwell and cloud allowance once. Continue within scope and collect deferred actions. Save progress on stop; resume requires an explicit request.

[Sessions](wiki/en/operations/browse.md) · [Controls](wiki/en/operations/platforms.md) · [Vision](wiki/en/operations/vision.md) · [Acquisition](wiki/en/operations/acquisition.md) · [Analysis](wiki/en/operations/workflow.md) · [Recovery](wiki/en/operations/recovery.md)

Retain source code, runtime, private configuration and imported originals. After review, clean task-owned video/audio/frames/images and registered download copies. Durable output is MD/JSON with native timing, evidence indexes, request and cleanup records.

## Cases and validation scope

Historical real [short-video](docs/cases/short.en.md), [long-video](docs/cases/long.en.md) and [image-post](docs/cases/note.en.md) summaries remain available. Current offline, terminal, browser, cloud and other-device evidence is separated in [acceptance](wiki/shared/acceptance/overview.md). TikTok is untested this round. Acquisition depends on actual platform/source conditions.

## Agent documentation and licensing

[AGENTS.md](AGENTS.md), [SKILL.md](SKILL.md), [machine index](docs/agent/index.json) and [llms.txt](llms.txt) route by intent. The [OKF Wiki](wiki/index.md) provides modular knowledge; private cases stay local. Original code uses [MIT](LICENSE); see [third-party notices](THIRD_PARTY_NOTICES.md). Third-party works retain their existing rights.

This run verified parser acquisition, understanding, review and cleanup for Douyin, YouTube, Xiaohongshu and Bilibili video/selected part/image post. Full-playback evidence is listed separately. Real Chrome/Edge combinations, WorkBuddy bridge repair and v2.5.0 clean-device installation remain pending; see [v2.5.0 evidence](wiki/shared/acceptance/v25.md).
