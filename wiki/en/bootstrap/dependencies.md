---
{
  "type": "Runbook",
  "title": "Source and dependencies",
  "description": "Source and dependencies — douyin-agent operational knowledge",
  "tags": [
    "douyin-agent",
    "en",
    "bootstrap",
    "dependencies"
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


# Source and dependencies

Prerequisites: inspect actual host file, terminal, network-reading and browser capabilities; do not invent tool names. This path targets Windows x64; other systems/architectures need separate validation.

## Obtain an ordinary directory without Git/Python/Conda

Read repository `fetch.ps1` through the browser/network tool and save it at a new short path. It uses Windows PowerShell 5.1/7 to download only delivery.json allowlisted files from a fixed release tag; it does not execute downloaded code. Git and archives are unnecessary.

```powershell
Invoke-WebRequest -UseBasicParsing 'https://raw.githubusercontent.com/HNNUYUXUAN/douyin-agent/v2.5.0/fetch.ps1' -OutFile './fetch.ps1'
# Inspect the script before execution; replace the destination with the selected path.
./fetch.ps1 -Destination 'D:\da\repo' -Ref 'v2.5.0'
```

Without D:, choose a writable short user-directory path. If downloading is blocked, the host can obtain delivery.json and its files individually from the same GitCode version, or reuse available Git. Record the actual source/version; do not mix mirrors. A failed fetch may leave an incomplete new directory; preserve it for inspection and retry in a different new directory. Review the public tag and scripts before installation.

## Conda

Discover existing Conda first. If absent, open the [official Miniconda guide](https://www.anaconda.com/docs/getting-started/miniconda/install) and [official releases](https://repo.anaconda.com/miniconda/); select Windows x86-64 and verify publisher SHA256/signature. Install for the current user at a separate short path and preserve global PATH.

Within installation authorization the host may run the official installer. For interactive installation choose Just Me and disable global Python registration/PATH modification. Official silent arguments are `/InstallationType=JustMe /RegisterPython=0 /AddToPath=0 /S /D=ABS_PATH`; `/D` must be last and unquoted, requiring a path without spaces. User handles license confirmation, login, organization-policy and OS authorization prompts. Locate conda.exe again afterward instead of relying on the old terminal PATH. Base Python 3.10+ is required.

## FFmpeg / FFprobe

Check executable paths and versions. If absent, open the [official FFmpeg Windows downloads](https://ffmpeg.org/download.html#build-windows), follow a linked build provider, and verify source/hash. Extract both ffmpeg.exe and ffprobe.exe under workspace `tools/ffmpeg/bin/`. The CLI adds this pair to its process PATH; global installation is unnecessary. Existing reliable PATH tools can be reused.

## Check afterward

Install through the [WorkBuddy guide](workbuddy.md), then run doctor and onboard --check. Verify Python 3.12, both media tools and key presence separately, without paid service calls. Record exact download/policy blockers through the [knowledge entry](knowledge.md).

Installer arguments: [official Conda Windows guide](https://docs.conda.io/projects/conda/en/stable/user-guide/install/windows.html) and [Constructor options](https://conda.github.io/constructor/cli-options/).


If raw is unreachable, obtain fetch.ps1 through `https://api.github.com/repos/HNNUYUXUAN/douyin-agent/contents/fetch.ps1?ref=v2.5.0`, decode Base64 content and review before execution. The script resolves a fixed commit and falls back to the official codeload ZIP, extracts allowlisted files and removes the temporary archive. Retry into a new directory, retaining the failed state. pip output is forwarded; PIP_INDEX_URL can explicitly choose a trusted source. Record its sanitized origin locally, never credential-bearing values.


## Official distribution unavailable

For Miniconda record the selected fixed version, official HTTPS origin and actual installer SHA256. When official hashes are unavailable, require a Valid Authenticode signature from Anaconda and explicitly record the missing official digest comparison. Use FFmpeg builds listed by its official download page; BtbN is an alternative when gyan.dev is unavailable. Verify the matching publisher release checksum.

Diagnose unavailable screenshot APIs using browser recovery first. Where host capabilities permit, installed FFmpeg gdigrab can provide scoped public desktop evidence with ownership/cleanup records. Do not change system security policy for screenshots.
