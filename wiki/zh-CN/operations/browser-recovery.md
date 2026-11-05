---
{
  "type": "Runbook",
  "title": "WorkBuddy 浏览器故障分支",
  "description": "WorkBuddy 浏览器故障分支 — douyin-agent operational knowledge",
  "tags": [
    "WorkBuddy",
    "extension",
    "扩展",
    "offline",
    "离线",
    "screenshot",
    "截图",
    "timeout",
    "超时",
    "provider invocation timed out",
    "Current display surface not available for capture",
    "native messaging"
  ],
  "status": "active",
  "generated": {
    "by": "douyin-agent/2.5.0",
    "at": "2026-11-05T02:27:48.555869+00:00"
  },
  "sources": [
    {
      "resource": "https://gitcode.com/yuxuan6426/workbuddy-browser-bridge-okf/tree/779e3794e495293af3607f66f67a90d6832511b9"
    },
    {
      "resource": "https://developer.chrome.com/docs/extensions/develop/concepts/native-messaging"
    },
    {
      "resource": "https://learn.microsoft.com/en-us/microsoft-edge/extensions/developer-guide/native-messaging"
    }
  ],
  "applicability": {
    "skill": "2.5.x",
    "host": "capability-detected; see body for measured versions"
  },
  "verification_scope": "Documentation reviewed; runtime acceptance is recorded separately."
}
---

# WorkBuddy 浏览器故障分支

## 入口与适用范围

先按错误分类：扩展显示离线／WorkBuddy 没有运行、DOM 可读但截图超时、单个页面或播放器未加载。回传修复证据适用 Windows x64、WorkBuddy 5.9.3、扩展 0.2.8。其他版本先检查兼容性；新脚本的真机验证范围见发布验收记录。

## 扩展离线

检查 `.workbuddy` 内运行时、`com.workbuddy.extension` 清单、实际扩展 ID、Chrome/Edge 各自 HKCU NativeMessagingHosts 注册项和当前宿主日志。宿主进程存在与扩展连接分别判断。

脚本默认 `Check`，只读且不下载；`Plan` 读取官方 feed 并输出变更预览。`Repair` 按实际宿主版本选择兼容条目，仅从官方域名下载，校验 SHA256、版本和腾讯 Authenticode 签名。脚本备份受影响文件和注册项，合并指定插件配置，记录变更前后摘要；并发修改时停止覆盖。只注册当前使用的浏览器和已观察到的正式扩展 ID。

以实际路径、版本、扩展 ID 替换示例；优先 PowerShell 7，缺失时使用 Windows PowerShell 5.1。命令在实际技能根运行：

```powershell
./scripts/workbuddy-bridge.ps1 -Mode Check -Browser Chrome,Edge
./scripts/workbuddy-bridge.ps1 -Mode Plan -Browser Chrome -WorkBuddyVersion '5.9.3' -ExtensionId 'ajnnogdfpilbhkeggdjlcokgglijmdde' -Receipt 'D:\da\ops\bridge-01.json'
./scripts/workbuddy-bridge.ps1 -Mode Repair -Browser Chrome -WorkBuddyVersion '5.9.3' -ExtensionId 'ajnnogdfpilbhkeggdjlcokgglijmdde' -Receipt 'D:\da\ops\bridge-01.json'
./scripts/workbuddy-bridge.ps1 -Mode Rollback -Receipt 'D:\da\ops\bridge-01.json'
```

修复后用少量连接检查等待扩展重连，再由宿主重新列浏览器、读取实际作品 DOM、执行截图。注册项通过仅证明静态配置，截图和页面须分别实测。需要重启时保存现场并交给用户，保留浏览器进程。

## DOM 正常但截图超时

先记录失败接口、宿主和扩展版本，用同一公开页面分别核验 DOM 与截图。检查当前可见表面、标签授权和连接状态；最多两次有明确诊断目的的复测，持续失败保留错误。能够依靠 DOM 的独立步骤继续。桥接静态检查健康时走截图分支，不直接重铺运行时。

## 页面与播放器

刷新实时 DOM；点击播放并等待约 3–10 秒，少量检查进度。检查同站其他在播标签，先暂停本任务播放器；用户原有播放器需要协调，不自动关闭。再检查网络或可见拦截证据。`00:00/00:00` 和占位图只说明尚未确认起播。关闭本任务自动连播，保存结束状态后再切换。B 站 412 记页面访问受限，不启动 buvid／playurl 获取路线。

## 失败与恢复

签名、摘要、兼容性或路径校验失败时保留诊断；重跑先检查回执和状态。修复失败且产生了已记录变更，可用同一回执 `Rollback`；后续用户修改会阻止自动回滚。备份位于用户 `.workbuddy/bridge-backups/`，属于本地私人数据，不进入发布包。中断锁需核实原进程已结束后人工处理，再按记录恢复。两次有依据的修复仍失败时集中交接诊断，保留可用浏览器继续独立任务。


错误路由：`provider invocation timed out` 且 DOM 正常时先走截图分支；`Current display surface not available for capture` 检查可见捕获表面；扩展显示“WorkBuddy 没有在运行”才进入连接／Native Messaging 检查。Check 未提供实际扩展 ID 时匹配状态为 null。Plan/Repair 必须显式选择实际使用的浏览器。
