# Sources and dependencies
Original workflow/media code is adapted from this user's local douyin-understand baseline; no vendor/notes signature downloader is included.
Runtime dependencies (not vendored): Python PSF; requests Apache-2.0; python-dotenv BSD-3-Clause; Pillow MIT-CMU; websockets BSD-3-Clause; transitive dependency licenses follow their distributions. Miniconda/Conda and FFmpeg are externally installed and retain their own terms; FFmpeg builds vary.
Protocol references: https://docs.volcengine.com/docs/ark/agent-plan-personal-voice-model?lang=zh and https://github.com/volcengine/ark-cli/tree/c34435e716ba23e342e8a0318c02bcd72e5f4139/skills/arkcli-understand . Protocol independently implemented, no copied SDK/CLI package. Search uses documented Yuanbao/Bocha APIs. Test media stays local and is not licensed for redistribution.

Locked dependency license metadata is listed in references/dependency-licenses.json. It is an inventory, not a replacement for upstream license texts. Runtime binaries are rebuilt, not redistributed.

WorkBuddy bridge recovery guidance and the repair helper are adapted from the MIT knowledge package https://gitcode.com/yuxuan6426/workbuddy-browser-bridge-okf at commit 779e3794e495293af3607f66f67a90d6832511b9 (Copyright 2026 yuxuan6426). The permission notice is retained in references/bridge-license.txt. This distribution contains reviewed guidance and source scripts, not Tencent runtime binaries. The helper selects compatible official feed entries and verifies download hashes and Authenticode signatures before installation.
