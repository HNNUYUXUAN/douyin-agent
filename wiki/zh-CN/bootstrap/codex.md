---
{
  "type": "Runbook",
  "title": "Codex 宿主配置",
  "description": "Codex 宿主配置",
  "tags": [
    "codex",
    "host",
    "setup"
  ],
  "status": "stable",
  "generated": {
    "by": "douyin-agent/2.5.1",
    "at": "2026-11-05T09:44:27.533063+00:00"
  },
  "sources": [
    {
      "resource": "https://learn.chatgpt.com/docs/chrome-extension"
    }
  ],
  "applicability": {
    "skill": "2.5.1 candidate",
    "host": "Windows x64; recheck current host capabilities"
  },
  "verification_scope": "Candidate implementation; fixture, local and recipient results are recorded separately."
}
---

# Codex 宿主配置


## 触发与前置
首次配置或连接失效。先读首启必读包，使用实际宿主工具，不能套用另一宿主的命令。
## 执行
新安装技能目录为当前用户 `.codex/skills/douyin-agent`；已有安装沿用匹配回执。运行工作区和宿主会话目录分别记录。通过宿主技能列表／实际技能调用核对发现；新聊天未测试就单列待验收。
平台页面只用用户 Chrome／Edge 扩展实例，内置实例只用于公开解析站／说明页。按 Codex 实际已连接扩展和用户标签观察，不要求工具清单使用 WorkBuddy 的字段。
读取一个公开页 DOM 并截图，分别记录连接、DOM、截图和文件保存能力。安装配置不需要试下载作品；文件保存可保持 unverified，开工前补探测。未选平台不遍历登录页。
## 成功与上限
静态注册不等于连接通过；实时 DOM 与截图各有证据才记录 passed。发现不刷新或连接失败先读故障索引，不能反复安装。登录和凭据由用户本地操作。
## 停止与恢复
连接异常按浏览器手册分支；不能连接时保留安装结果，集中交接。浏览器通过后进入 Key 手册，缺 Key 必须等待。
