# WorkBuddy 安装与能力核验

Windows 先探测已有 Git Bash，再 PowerShell 7、Windows PowerShell 5.1；不为优先级自动安装新终端。
WorkBuddy 5.9.3 Windows Server 2022 异机回传已验证用户级 `.workbuddy/skills/douyin-agent` 的本会话发现；新聊天发现及云处理仍需另验。新安装默认用户级目录；已有安装复用 agent-context.json 与 installed.json 记录的实际路径。工作区可以独立于宿主自动生成的会话文件夹。

从源码根执行 `bash ./install.sh --workspace WORKSPACE --host workbuddy --conda CONDA_EXE`，或对应 `./install.ps1 -Workspace WORKSPACE -TargetHost workbuddy -Conda CONDA_EXE`。`--skill-dir` / `-SkillDir` 可显式指定目录。用户级路径以当前用户目录为准。

安装后让实际 WorkBuddy 按名称加载技能，分别记录技能发现、扩展、桌面桥接和实际作品页读取。5.9.3 回传中未发现下载原语，只证明那次工具集；每次运行重新探测能力，不猜工具。浏览器设置与连接按[官方文档](https://www.codebuddy.cn/docs/workbuddy/From-Beginner-to-Expert-Guide/Function-Description/Right-Sidebar)操作。

首次使用读 [first-run](first-run.md)，多平台与视觉读 [browse](../../../docs/agent/zh-CN/browse.md)。
