# Start from zero

Applies to a new Windows x64 device with only WorkBuddy and its Chrome/Edge connector installed. The standard entry filename is `SKILL.md`; scripts and references remain alongside it.

1. [Source and dependencies](dependencies.md): no preinstalled Git, Python or Conda is assumed. Inspect the actual shell; Windows PowerShell can fetch the source.
2. [WorkBuddy host setup](workbuddy.md): select a working folder, install into its `.codebuddy/skills/douyin-agent`, and verify client discovery plus real browser access.
3. [Onboarding](../../../docs/agent/en/onboarding.md): the host opens Douyin, Agent Plan purchase/console pages and local .env; the user signs in, purchases and enters the key.
4. [First task](../../../docs/agent/en/workflow.md): acquire a real work, pass integrity, show usage, execute within authorization, review and finalize.
5. [Troubleshooting and knowledge](knowledge.md): search guides/private cases, act on evidence and store a sanitized case.
6. [Clean-device acceptance](clean-test.md): record each observed result; missing evidence stays blocked or unverified.

Copyable first request:

```text
Install douyin-agent from https://github.com/HNNUYUXUAN/douyin-agent.
Read AGENTS.md, AGENT_INSTALL.md and references/bootstrap/en/first-run.md.
This is a new Windows device with only WorkBuddy and its browser connector. Detect and prepare source files, Conda Python 3.12, media tools and the WorkBuddy skill directory.
Open required pages for my login, purchase, local key entry or OS authorization. Preview actual sample usage before authorized validation.
Search the Wiki when problems occur; record reusable sanitized facts and outstanding issues.
```
