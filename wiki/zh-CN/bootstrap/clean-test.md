---
{
  "type": "Runbook",
  "title": "全新设备测试清单",
  "description": "全新设备测试清单 — douyin-agent operational knowledge",
  "tags": [
    "douyin-agent",
    "zh-CN",
    "bootstrap",
    "clean-test"
  ],
  "status": "active",
  "generated": {
    "by": "douyin-agent/2.5.0",
    "at": "2026-11-05T02:27:48.555869+00:00"
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

# 全新设备测试清单

起始条件：Windows x64，只安装 WorkBuddy 与其浏览器扩展；用户不预装 Git、Conda、Python、FFmpeg。不迁移作者配置、缓存或 ASR 结果。

1. 发 [首次请求](first-run.md)。记录 OS/架构、WorkBuddy 版本、实际终端与缺失依赖。
2. 宿主读取仓库、取得普通目录、校验版本，并自动准备或打开官方依赖安装入口。用户只处理必要系统授权、许可、登录和购买。
3. 使用 workbuddy 宿主参数安装；确认技能被当前 WorkBuddy 工作文件夹发现。
4. 浏览器扩展连接、桌面桥接、抖音页面实际读取分别记录。Chrome 与 Edge 只把本次使用的一种标为通过。
5. 打开 Agent Plan 页面和本地 .env，用户配置。doctor/onboard 仅本地检查，真实调用另记录。
6. 选择一条短公开视频，取得完整文件，展示具体预览，用户授权后运行、复核、finalize。检查只保留 MD/JSON、用户导入原件保留。
7. 重启 WorkBuddy，在同工作文件夹提问已有报告；验证能读取清理后文字。制造一个无害阻塞（如缺失 Key 的独立测试工作区），验证能检索 Wiki、记录本地案例并再次检索。
8. 按 [验收模板](../../../docs/agent/examples/clean-device.json) 记录每项 passed/blocked/unverified、时间和脱敏证据。把失败原因反馈给维护者，勿发送 Key 或整套私人日志。

本次仓库准备不能提前证明这次异机测试成功。只有用户新设备的实际证据才能更新 WorkBuddy、浏览器、云调用和异机状态。
