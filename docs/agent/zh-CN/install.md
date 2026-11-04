# 安装与升级

[English](../en/install.md) · [索引](../index.json)

新 WorkBuddy 设备先读 [从零引导](../../../references/bootstrap/zh-CN/first-run.md)，使用明确的 `-TargetHost workbuddy` / `--host workbuddy`，勿沿用 Codex 默认技能目录。

## 适用意图

从仓库首次安装技能，或升级已有安装并重建独立环境。

## 前置条件

宿主可访问本地文件与终端，已取得用户选择的源码版本；Windows 为首测环境。先识别已有安装和依赖，缺项按下文官方入口处理。

## 最少输入

仓库来源/版本、可写工作区、宿主技能目录；需要指定已有 Conda 时提供其可执行路径。安装阶段不需要把 Key 交给 Agent。

## 操作步骤

适用对象：接收仓库链接并负责安装的宿主 Agent。先读根目录 [AGENTS.md](../../../AGENTS.md)。本流程以 Windows Codex 为基线；不要把可读取仓库等同于浏览器或云服务已可用。

1. 从用户给出的 [GitHub](https://github.com/HNNUYUXUAN/douyin-agent) 或 [GitCode](https://gitcode.com/yuxuan6426/douyin-agent) 获取同一版本的普通目录，核对 `SKILL.md`、`delivery.json`、脚本和锁文件。记录来源与版本；不混用镜像文件。
2. 确认宿主技能目录。工作区与技能目录分开：有 D: 时建议 `D:\douyin-agent`，否则选择其他可写短路径。新增名称使用短 ASCII；工作区根路径不超过 85 字符，为任务后缀预留空间，完整路径不超过 160 字符。
3. 检查用户所选 Windows PowerShell 5.1、PowerShell 7 或 Git Bash 的实际路径与版本，复用系统或宿主随附工具；检查已有 Conda（基础 Python 3.10+）和 FFmpeg/FFprobe。安装器复用 Conda 并在工作区创建独立 Python 3.12 环境。缺少 Conda 时打开 [Miniconda 官方说明](https://www.anaconda.com/docs/getting-started/miniconda/install)；FFmpeg 获取方式以 [官方入口](https://ffmpeg.org/download.html) 为准。需要用户安装的步骤具体指出，不用缺配置触发收费请求。
4. 在仓库根执行，替换为实际目录：

```powershell
./install.ps1 -Workspace 'D:\douyin-agent' -SkillDir 'C:\Users\YOUR_USER\.codex\skills\douyin-agent'
```

`setup.ps1 -Workspace WORKSPACE` 是已有源码的环境重建入口；它不等同于把技能安装进宿主发现目录。需要显式指定已安装 Conda 时，setup 支持 `-Conda CONDA_EXE`。


Git Bash 使用同一安装核心：

```bash
bash ./install.sh --workspace '/d/douyin-agent' --skill-dir '/c/Users/YOUR_USER/.codex/skills/douyin-agent'
```

Conda 顺序为显式 `-Conda` / `--conda` → `CONDA_EXE` → PATH → 用户目录与 ProgramData 的常见 Miniconda/Anaconda/Miniforge 位置。Git Bash 接受 `/d/...` 和 Windows 路径，含空格需加引号；不要用 WSL Bash 替代。运行时直接使用工作区解释器，无需激活 Conda。

只准备环境也可运行 `bash ./setup.sh --workspace '/d/douyin-agent' --conda '/c/PATH_TO_CONDA/Scripts/conda.exe'`；省略 Conda 参数会自动发现。PowerShell 执行受设备策略阻止时报告具体原因，由用户按设备管理要求处理。

5. 根据安装结果定位 Python 和技能根目录；后续统一使用 `PYTHON SKILL/scripts/da.py --workspace WORKSPACE COMMAND`，路径含空格须引用。
6. 进入 [首次使用](onboarding.md)，先 `onboard --check`，再由宿主实际检查浏览器。仅本地 `doctor` 成功，不能声明完成真实服务验证。

升级前核对上一安装回执的文件哈希，保留用户修改、未知新增文件和 `.env`。代码回滚备份在技能发现目录之外。不要删库重装或覆盖整套工作区来解决冲突。最终检查新版本文件、独立环境路径和本地配置是否对应。

安装完成后的自然语言发现按宿主实际行为验证；需要刷新时提示刷新。现有聊天成功与全新聊天成功分别记录。


安装分为环境准备和文件事务。已准备的环境及新建配置在失败后保留，便于修复重试；既有 `.env` 不覆盖。文件事务覆盖技能文件、退休文件、安装回执、workspace.json 和 agent-context.json，失败恢复旧内容；恢复失败记录 backup/recovery.json。退休文件仅在旧回执哈希匹配后备份并移除，未知用户文件保留。安装成功后两份工作区记录均指向实际安装目录。

## 预期输出与成功依据

安装回执和实际技能目录/工作区对应；源码发布哈希、Python 路径及本地依赖检查可核对。浏览器、云服务和自然语言发现状态分别验证，不随安装自动判为通过。

## 停止或恢复条件

遇到用户文件修改冲突、未知已有目录、无可用环境或路径越界时停止覆盖，保留现场；按 [恢复指南](recovery.md) 区分环境与任务问题。

## 下一步链接

继续 [首次使用](onboarding.md)，就绪后进入 [取得作品](acquisition.md) 与 [任务流程](workflow.md)。


v2.4：终端按已有 Git Bash → PowerShell 7 → Windows PowerShell 5.1 选择，记录实际路径/版本。WorkBuddy 新安装使用用户级 `.workbuddy/skills/douyin-agent`，已有安装沿用回执；会话目录和运行工作区分开。时间戳以系统 UTC 为准。新增平台/视觉/浏览流程从 [会话指南](browse.md) 按需加载。下载和检索为两层：免费解析站优先；寻找来源用已有检索技能 → 宿主搜索 → 已配置元宝/博查。缺少检索能力时打开服务官方入口，让用户本地配置 Key。`parsed_download_failed` 表示解析成功但文件未落地，所有来源尝试均计入每轮三源上限。用户协助提供本地文件后保留原件，重新核对身份、首尾、时长或图片顺序。不要读取未知剪贴板来寻找下载地址。

可先用 Windows 自带 PowerShell 执行 `scripts/terminal.ps1`，它只读返回首选终端的路径和版本；然后用返回的终端执行安装。
