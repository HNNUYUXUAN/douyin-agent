# WorkBuddy host setup

WorkBuddy and CodeBuddy CLI are different entrypoints. Use actual WorkBuddy tools; do not reuse Codex @Chrome tool names. Verify extension installation, desktop bridge, session-tab access and Douyin login separately.

## Location and command

The official project guide supports `.codebuddy/skills/` under the working directory. Set the selected workspace as WorkBuddy's working folder first, then run:

```powershell
./install.ps1 -Workspace 'D:\da' -TargetHost workbuddy -Conda 'C:\PATH\Scripts\conda.exe'
```

Git Bash: `bash ./install.sh --workspace '/d/da' --host workbuddy --conda '/c/PATH/Scripts/conda.exe'`. Windows PowerShell works without Git Bash. WorkBuddy mode defaults to `WORKSPACE/.codebuddy/skills/douyin-agent`; explicit `-SkillDir` / `--skill-dir` overrides it. Omitting the host retains Codex defaults, so WorkBuddy installation must specify its host or actual directory.

Confirm SKILL.md, scripts, references and dependency files exist. Have WorkBuddy reload the working folder and actually list or invoke douyin-agent. File copying alone does not prove discovery. If the client does not read this location, follow its current official project configuration and record version/status; do not infer hidden paths or equate IDE documentation with observed client behavior.

## Browser

In WorkBuddy Settings → Agent → Browser Control, verify the chosen Chrome/Edge extension and desktop bridge. Only explicitly opened/shared session tabs are controlled. Ask the host to open Douyin and read the actual page; the user handles login/CAPTCHA. Installed extension, connected bridge, readable tab and logged-in site are separate outcomes.

Sources: [project and skill directories](https://www.codebuddy.cn/docs/workbuddy/From-Beginner-to-Expert-Guide/Function-Description/Project), [browser operations](https://www.codebuddy.cn/docs/workbuddy/From-Beginner-to-Expert-Guide/Function-Description/Right-Sidebar), [Chrome extension](https://chromewebstore.google.com/detail/workbuddy/ajnnogdfpilbhkeggdjlcokgglijmdde). Open Edge's installation entry from WorkBuddy's current browser list.

Next: [service onboarding](../../../docs/agent/en/onboarding.md). Record actual clean-device WorkBuddy execution using the [acceptance checklist](clean-test.md).
