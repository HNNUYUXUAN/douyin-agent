# WorkBuddy 宿主配置

WorkBuddy 与 CodeBuddy CLI 是不同入口。使用 WorkBuddy 实际工具，不能套用 Codex 的 @Chrome 工具名。浏览器连接器安装、桌面端桥接、会话标签页访问和抖音登录逐项核验。

## 技能位置与命令

官方项目说明支持工作目录下 `.codebuddy/skills/`。先将所选工作区设为 WorkBuddy 当前工作文件夹，再运行：

```powershell
./install.ps1 -Workspace 'D:\da' -TargetHost workbuddy -Conda 'C:\PATH\Scripts\conda.exe'
```

Git Bash 等价：`bash ./install.sh --workspace '/d/da' --host workbuddy --conda '/c/PATH/Scripts/conda.exe'`。未装 Git Bash 时直接使用 Windows 自带 PowerShell。WorkBuddy 模式默认技能目录是 `WORKSPACE/.codebuddy/skills/douyin-agent`；`-SkillDir` / `--skill-dir` 可显式覆盖。未指定宿主时保留 Codex 兼容默认值，因此 WorkBuddy 安装必须明确传宿主或目录。

确认目录内有 SKILL.md、scripts、references 和依赖文件。让 WorkBuddy 重新读取该工作文件夹并实际列出或调用 douyin-agent；仅复制成功不算发现通过。客户端若不读取此目录，用当前版本官方项目级配置说明处理并记录版本/状态，不猜测隐藏路径，不把 CodeBuddy IDE 路径当另一个客户端的实测。

## 浏览器

进入当前 WorkBuddy 设置 → 智能体 → 浏览器操控，核对 Chrome/Edge 扩展与桌面桥接已连接。扩展只控制会话明确打开或共享的标签页。让宿主打开抖音并读到实际页面，用户按需登录/处理验证码。扩展存在、桥接连接、标签页可读、网站已登录是四项不同结果。

官方依据：[项目与技能目录](https://www.codebuddy.cn/docs/workbuddy/From-Beginner-to-Expert-Guide/Function-Description/Project)、[浏览器操作](https://www.codebuddy.cn/docs/workbuddy/From-Beginner-to-Expert-Guide/Function-Description/Right-Sidebar)、[Chrome 扩展](https://chromewebstore.google.com/detail/workbuddy/ajnnogdfpilbhkeggdjlcokgglijmdde)。Edge 入口从 WorkBuddy 当前浏览器列表打开，避免使用猜测的商店地址。

下一步：[首次服务配置](../../../docs/agent/zh-CN/onboarding.md)。安装入口与文档的 WorkBuddy 适配已检查；真实 WorkBuddy 全新设备执行状态须由 [验收清单](clean-test.md) 记录。
