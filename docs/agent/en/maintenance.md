# Maintenance, acceptance and release

[中文](../zh-CN/maintenance.md) · [Index](../index.json)

## Applicable intent

Maintain bilingual documentation, implementation and public assets; validate changes and prepare ordinary-directory releases or installation upgrades.

## Prerequisites

The change/publication authorization is clear, and actual source plus relevant evidence are available. Follow repository AGENTS.md before starting.

## Minimum inputs

Change scope, target version/commit, affected capabilities and evidence. Public assets also need publication eligibility and source information.

## Procedure

Read [AGENTS.md](../../../AGENTS.md), the relevant runtime scripts and both language guides. README serves users; detailed operations belong here. Keep `index.json` and `llms.txt` aligned with real files and supported commands.

For installation/onboarding changes, cover first/repeated installs, modified-file conflicts, configuration preservation, missing Conda/FFmpeg, read-only checks, host-record updates and path reuse after restart. For runtime changes run `PYTHON scripts/test_da.py`, adding tests that cover meaningful risks. Preview real calls first; do not use production jobs as read-only health checks.

Record structural/doc checks, offline tests, actual browser behavior, actual Agent Plan calls, same-machine relocation, fresh-chat discovery and other-device results separately. Screenshots must show real behavior; label conceptual illustrations rather than treating them as validation. Example reports and motion demos contain only authorized, sanitized public content, without third-party original videos, private prompts, account pages or Keys.

Export an ordinary directory using the `delivery.json` allowlist; add required guides and accepted assets to that manifest. Exclude test-generated `__pycache__` and other non-release files; never upload the whole workspace. Check bilingual links, images at source/display sizes, copyable commands, licenses and attribution. Keep maintainable diagram sources and concise public provenance; private process records stay in the private workspace.

The source repository is [GitHub](https://github.com/HNNUYUXUAN/douyin-agent), with [GitCode](https://gitcode.com/yuxuan6426/douyin-agent) also provided. Record the actual published commit/version and mirror state. Do not claim publication before a successful push and remote presentation check. Documentation work must not silently change visibility or licensing.

Upgrades still compare receipt hashes and preserve rollback code, user `.env` and workspace state. Media cleanup cannot be rolled back. Release notes and [acceptance evidence](../../../references/acceptance.md) must agree about validated and untested capabilities.

For installer changes, also run `scripts/test_installer.py` and exercise install, repeat install, setup, and read-only entrypoints through Windows PowerShell 5.1, PowerShell 7, and Git Bash. README diagram sources are native Mermaid blocks; check rendering on both platforms and keep complete text steps.

## Expected outputs and success evidence

Documentation, commands, index, delivery manifest and implementation agree, with separate test/presentation records. Publication requires actual commit/push and remote checks; local files alone are insufficient.

## Stop or recovery conditions

On secrets, unauthorized assets, file conflicts, failed tests or unverified remote state, preserve work and stop the affected publication/overwrite step while recording the gap. Diagnose runtime issues through [recovery](recovery.md).

## Next links

Use [installation](install.md) for distribution, [onboarding](onboarding.md) for recipient verification and the [workflow](workflow.md) for functional checks.
