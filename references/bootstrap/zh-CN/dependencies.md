# 源码与依赖

前置条件：宿主实际具备本地文件、终端、联网读取和浏览器工具；先检查这些能力，不猜工具名。此链路面向 Windows x64；其他系统或架构需独立验证。

## 无 Git、Python、Conda 时获取普通目录

宿主通过浏览器或联网读取取得仓库的 `fetch.ps1`，检查源码后保存到一个新建短路径。该脚本仅依赖 Windows PowerShell 5.1/7，从固定发布标签下载 delivery.json 白名单文件；不执行下载的代码。无需 Git，也不创建压缩包。

```powershell
# 在实际选定目录执行；ROOT 由宿主替换为短路径
Invoke-WebRequest -UseBasicParsing 'https://raw.githubusercontent.com/HNNUYUXUAN/douyin-agent/v2.3.0/fetch.ps1' -OutFile './fetch.ps1'
# 先读取并核对脚本，再执行
./fetch.ps1 -Destination 'D:\da\repo' -Ref 'v2.3.0'
```

没有 D 盘时使用用户目录下可写短路径；不得照抄作者路径。下载受阻时，宿主从 GitCode 同版本逐文件取得 delivery.json 与白名单文件，或复用已有 Git 克隆；记录实际来源与版本，不混用镜像文件。脚本失败可能留下不完整新目录，保留并检查，重试使用另一新目录。下载完成不等于来源验证；对照公开标签、检查脚本后安装。

## Conda

先按安装器顺序探测已有 Conda。缺失时由宿主打开 [Miniconda 官方安装说明](https://www.anaconda.com/docs/getting-started/miniconda/install) 和 [官方发行目录](https://repo.anaconda.com/miniconda/)，选择 Windows x86-64 安装器，校验官方 SHA256/签名。只安装当前用户、独立短路径，保留现有全局 PATH。

宿主在用户安装授权覆盖范围内可运行官方安装器。交互安装选择 Just Me、取消注册全局 Python 和修改 PATH；静默安装按官方文档的 `/InstallationType=JustMe /RegisterPython=0 /AddToPath=0 /S /D=ABS_PATH` 参数，`/D` 放最后且不能带引号，故安装位置需无空格。登录、许可确认、组织策略或系统授权弹窗交给用户。完成后重新定位 conda.exe，不依赖旧终端 PATH。安装器基础 Python 需 3.10+。

## FFmpeg / FFprobe

检查实际命令和版本。缺失时打开 [FFmpeg 官方 Windows 下载入口](https://ffmpeg.org/download.html#build-windows)，只从其链接的构建方取得 Windows x64 包，检查来源与哈希。由宿主解包到工作区 `tools/ffmpeg/bin/`，其中必须同时有 ffmpeg.exe、ffprobe.exe；本地 CLI 自动将此目录加入本进程 PATH，无需全局安装。已有可靠 PATH 工具可直接复用。

## 安装后检查

按 [WorkBuddy 指南](workbuddy.md) 安装后运行 doctor 和 onboard --check，分别核对 Python 3.12、FFmpeg、FFprobe、Key 状态；不调用收费服务。下载或系统策略受阻时记录准确错误，按 [知识入口](knowledge.md) 保存阻塞，不降级冒充验证通过。

安装参数依据：[Conda 官方 Windows 安装](https://docs.conda.io/projects/conda/en/stable/user-guide/install/windows.html) 和 [Constructor 参数](https://conda.github.io/constructor/cli-options/)。
