---
{
  "type": "Runbook",
  "title": "安装、终端与源码故障",
  "description": "安装、终端与源码故障",
  "tags": [
    "install",
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

# 安装、终端与源码故障

触发：终端错误、原生 stderr 中断、源码不可达、半安装、目录冲突、慢依赖或离线测试找不到 FFmpeg。
适用：Windows Git Bash／PowerShell 5.1／7，技能 2.5.x；用户回传宿主 5.9.3 的观察只证明该次环境。
前置：读 preflight、安装回执、最后 progress 阶段，保留 .env 和未知文件。仅记录白名单变量是否存在，不打印 env／set／完整宿主配置。
执行：
1. Git Bash 已有则用它；没有用已有 PowerShell 7，再用 5.1，不为优先级额外装终端。Conda 用显式路径、CONDA_EXE、PATH、工作区 tools 及常见位置发现，不全盘搜索。
2. raw 不可达：按依赖指南使用官方 API 和固定提交 codeload 白名单回退；使用同一来源提交，不混镜像。
3. PS5 的 `2>&1 | Tee-Object` 场景依赖现有 launch 临时隔离错误策略并恢复，以退出码判断，不把警告当失败。若仍失败，保存原生退出码和阶段，不能只删除日志重试。
4. 环境已建而技能未完成：确认无活动安装，按同一安装命令重跑一次，复用环境。文件哈希冲突／未知目录停止覆盖，保留诊断，不删工作区。
5. pip 持续输出时等待原命令，不重开安装。需要包源时只使用明确可信来源并脱敏记录；不改全局配置。脚本位置警告已由 --no-warn-script-location 关闭，其他错误照常输出。
6. 仅维护验收运行 `PYTHON SKILL/scripts/test_all.py --workspace WORKSPACE`，它配置本进程 FFmpeg 路径并检查两工具。普通安装不运行测试矩阵。
成功：安装退出 0、回执版本和实际目录对应；配置及未知文件保留。本地检查不证明云服务／新聊天。
上限：同一已诊断原因解决后重跑一次；重复失败停止并记录阶段、保留资源及恢复命令。
停止／恢复：缺 Conda 读 [Conda](conda.md)；桥接读 [连接](../operations/browser-recovery.md)；未知读 [交接](unknown.md)。


补充可观察故障：PS7 父进程传入模块路径时，PS5 可能报 Get-FileHash 不存在。Windows 专有脚本在 PS5 进程内显式从 PSHOME/Modules 加载本机 Utility/Security；不改全局 PSModulePath。仍失败保留模块错误，不自行复制 PS7 模块。


Current runtime procedure / 当前运行流程：[v2.5.1](../operations/transfer.md).
