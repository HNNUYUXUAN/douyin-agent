---
{
  "type": "Runbook",
  "title": "源码与依赖",
  "description": "源码与依赖 — douyin-agent operational knowledge",
  "tags": [
    "douyin-agent",
    "zh-CN",
    "bootstrap",
    "dependencies"
  ],
  "status": "active",
  "generated": {
    "by": "douyin-agent/2.5.1",
    "at": "2026-11-05T09:57:06.630627+00:00"
  },
  "sources": [
    {
      "resource": "https://github.com/GoogleCloudPlatform/knowledge-catalog/blob/62432a095456147ee71e70ac6e4dc0d2dea3ac30/okf/SPEC.md"
    }
  ],
  "applicability": {
    "skill": "2.5.x",
    "host": "capability-detected; see body for measured versions"
  },
  "verification_scope": "Documentation reviewed; runtime acceptance is recorded separately."
}
---


# 源码与依赖

前置条件：宿主实际具备本地文件、终端、联网读取和浏览器工具；先检查这些能力，不猜工具名。此链路面向 Windows x64；其他系统或架构需独立验证。

## 无 Git、Python、Conda 时获取普通目录

宿主通过浏览器或联网读取取得仓库的 `fetch.ps1`，检查源码后保存到一个新建短路径。该脚本仅依赖 Windows PowerShell 5.1/7，从固定发布标签下载 delivery.json 白名单文件；不执行下载的代码。无需 Git，也不创建压缩包。

```powershell
# 在实际选定目录执行；ROOT 由宿主替换为短路径
Invoke-WebRequest -UseBasicParsing 'https://raw.githubusercontent.com/HNNUYUXUAN/douyin-agent/v2.5.0/fetch.ps1' -OutFile './fetch.ps1'
# 先读取并核对脚本，再执行
./fetch.ps1 -Destination 'D:\da\repo' -Ref 'v2.5.0'
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


raw 不可达时，先从 `https://api.github.com/repos/HNNUYUXUAN/douyin-agent/contents/fetch.ps1?ref=v2.5.0` 取得脚本，解码 JSON 的 Base64 content，审阅后执行。脚本将标签解析为固定提交，回退 codeload 的官方 ZIP，仅解包白名单并清理临时归档。重试选择新目录，保留失败现场。pip 日志直接转发；可显式使用 PIP_INDEX_URL 指定可信包源，并在本地脱敏记录来源，避免输出含凭据的配置值。


## 官方供应源受阻

Miniconda 记录所选固定版本、官方 HTTPS 来源和实际安装器 SHA256。官方校验清单不可用时，确认 Authenticode 为 Valid 且签名者为 Anaconda 后方可使用，并标明未与官方摘要比对。FFmpeg 优先官方页面列出的构建；gyan.dev 不可达时可选同页 BtbN，按该构建发布的校验清单核验，不混用构建方摘要。

宿主截图 API 不可用时先按浏览器恢复指南诊断。确需桌面证据且宿主支持时，可使用已安装 FFmpeg 的 gdigrab；只采集任务相关公开区域，保存所有权和清理记录，不为取证改系统安全策略。

## 固定等待与恢复入口

缺 Conda 时完整读 [校验与等待手册](../faults/conda.md)，使用 scripts/install-conda.ps1 封装命令，不直接调用 NSIS 后立即返回。先取得官方固定版本安装器、记录 SHA256 并校验签名；不覆盖已有半成品。FFmpeg 供应源失败按 [安装故障](../faults/install.md) 处理。普通安装不运行离线套件或收费样例。
