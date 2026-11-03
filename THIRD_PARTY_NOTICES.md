# Sources and dependencies
Original workflow/media code is adapted from this user's local douyin-understand baseline; no vendor/notes signature downloader is included.
Runtime dependencies (not vendored): Python PSF; requests Apache-2.0; python-dotenv BSD-3-Clause; Pillow MIT-CMU; websockets BSD-3-Clause; transitive dependency licenses follow their distributions. Miniconda/Conda and FFmpeg are externally installed and retain their own terms; FFmpeg builds vary.
Protocol references: https://docs.volcengine.com/docs/ark/agent-plan-personal-voice-model?lang=zh and https://github.com/volcengine/ark-cli/tree/c34435e716ba23e342e8a0318c02bcd72e5f4139/skills/arkcli-understand . Protocol independently implemented, no copied SDK/CLI package. Search uses documented Yuanbao/Bocha APIs. Test media stays local and is not licensed for redistribution.

Locked dependency license metadata is listed in references/dependency-licenses.json. It is an inventory, not a replacement for upstream license texts. Runtime binaries are rebuilt, not redistributed.
