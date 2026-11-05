---
{
  "type": "Runbook",
  "title": "Conda 校验、安装等待与残留",
  "description": "Conda 校验、安装等待与残留",
  "tags": [
    "conda",
    "fault",
    "troubleshooting",
    "故障"
  ],
  "status": "stable",
  "generated": {
    "by": "douyin-agent/2.5.1",
    "at": "2026-11-05T09:44:27.533063+00:00"
  },
  "sources": [
    {
      "resource": "../../shared/acceptance/field-v251.md"
    },
    {
      "resource": "https://github.com/GoogleCloudPlatform/knowledge-catalog/blob/62432a095456147ee71e70ac6e4dc0d2dea3ac30/okf/SPEC.md"
    }
  ],
  "applicability": {
    "skill": "2.5.1 candidate",
    "host": "Windows x64; recheck current host capabilities"
  },
  "verification_scope": "Candidate implementation; fixture, local and recipient results are recorded separately."
}
---

# Conda 校验、安装等待与残留

触发：缺 Conda、安装器提前返回、目标只有半成品；适用 Windows x64 官方 Miniconda 安装器。
前置：先发现已有 Conda。缺失时从官方固定版本取得安装器，记录 SHA256；核对官方摘要，清单不可用时记录未比对，并要求 Valid 的 Anaconda Authenticode。来源、摘要或签名异常时停止。
执行：审阅 scripts/install-conda.ps1 后，在一个宿主命令生命周期内运行 `./scripts/install-conda.ps1 -Workspace ABS_ROOT -Installer ABS_EXE -Sha256 RECORDED_HASH`。目标固定为工作区 tools/miniconda3；路径无空格，JustMe、不改全局 PATH、不注册系统 Python。用户处理许可或系统授权。
脚本使用隐藏启动、轮询进度与实际 Conda/Python 检查，最长 900 秒。父安装器提前退出不等于就绪，须等 conda.exe 和基础 Python 可执行。宿主必须让原命令继续，按其任务句柄查看进度，不另起重复安装。
已有完整目标直接复用；已有不完整目标拒绝覆盖。超时保留进程与日志，先检查原安装是否还活跃。脚本不自动删除；确需清理必须核对绝对路径、该目录为本任务新建且无用户内容，再由维护流程处理。
成功：安装器成功退出且 conda --version、基础 Python>=3.10 均通过，或原有安装复用通过。
上限：一次安装；有新证据并排除原进程后才允许一次修正重跑。相同半成品不反复删装。
停止／恢复：摘要／签名异常直接交接；超时按记录恢复，保留有效环境，不下载其他运行时替代。
