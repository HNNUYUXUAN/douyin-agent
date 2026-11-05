---
{
  "type": "Runbook",
  "title": "观察、知识与会话回执故障",
  "description": "观察、知识与会话回执故障",
  "tags": [
    "records",
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

# 观察、知识与会话回执故障

触发：sources 被拒、时间超前、验收模板不能导入、登录墙无作品 ID、会话授权或检索结果异常。适用 v1/v2 回执和 2.5.x 兼容任务。
前置：先看实际命令 --help、机器索引及错误字段，不把完整验收表直接当 onboard 输入。
执行：知识来源接受已有工作区 MD/JSON 的裸相对路径或 workspace: 前缀；防越界继续有效。时间读实际系统钟，不能用会话估计时间。onboard 只提取 checks 中 status/observed_at/evidence；null 时间不导入，设备安装项目留验收表。
登录墙无规范 ID 时写会话 pending，不虚构作品。授权绑定会话与配置，旧会话保持兼容；不复制另一个会话的授权。检索先用故障索引或 `knowledge.py route --code CODE --language zh-CN`，再用短关键词 search；正文命中不证明当次修复已通过。
保存案例使用 knowledge.py record 的八字段模板；只写可观察现象、动作、结果和来源。成功／失败均可记 draft，不自动公开。检查字段白名单，禁止 env 全量输出、剪贴板、凭据、签名链接、账号和原始私有日志。
成功：校验接受真实证据，记录可重新检索；旧任务仍可读，未决请求不改变。
上限：纠正实际格式一次再提交；重复失败集中交接，不改校验器绕过保护。
停止／恢复：恢复前读实时 status 与原未决占用；缺文件或错误时保留事实，再按 [恢复协议](../../shared/recovery-protocol.md)。
