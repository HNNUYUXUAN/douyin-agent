# WorkBuddy installation and capability checks

On Windows prefer existing Git Bash, then PowerShell 7, then Windows PowerShell 5.1. Do not install a shell merely for priority.
The Windows Server 2022 / WorkBuddy 5.9.3 field report verified user-level `.workbuddy/skills/douyin-agent` discovery within its session. Fresh-chat discovery and cloud processing require separate evidence. New installations default to that user directory; existing installations reuse receipt/context paths. Runtime workspace is separate from the host's auto-created session folder.

From the source root use `bash ./install.sh --workspace WORKSPACE --host workbuddy --conda CONDA_EXE` or `./install.ps1 -Workspace WORKSPACE -TargetHost workbuddy -Conda CONDA_EXE`. Override with --skill-dir / -SkillDir. Resolve the actual current user home.

Have actual WorkBuddy load the installed skill by name. Record discovery, extension, desktop bridge and work-page reading separately. No download primitive appeared in that 5.9.3 field toolset; probe current capabilities rather than generalizing or inventing tools. Follow [official browser documentation](https://www.codebuddy.cn/docs/workbuddy/From-Beginner-to-Expert-Guide/Function-Description/Right-Sidebar).

Start with [first-run](first-run.md); multi-platform/vision routes begin at [browse](../../../docs/agent/en/browse.md).
