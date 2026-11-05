---
{
  "type": "Runbook",
  "title": "解析、无结果与文件取得故障",
  "description": "解析、无结果与文件取得故障",
  "tags": [
    "acquisition",
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

# 解析、无结果与文件取得故障

触发：无下载原语、页面仅广告、直链 403、解析成功但文件未落地。适用免费解析站；WorkBuddy 5.9.3 回传中 B 站 GreenVideo 浏览器下载成功、SnapAny 视频链接 403，是当次结果而非长期保证。
前置：开工后先探测宿主下载、已有下载技能、现有 curl 及确切文件回执能力；有工具不代表保存通过。复用验证过的站点，失效再按已有检索技能→宿主搜索→已配置元宝／博查发现。
执行：
1. 每作品原轮次最多三个不同站点。进入前 attempting；同站换路径／浏览器／传输保留同轮；登录墙、验证码、失败也计数。第一站失败不等于三站耗尽；不得自动新开一轮。
2. 按页面输入并回读。等待结果后只有推广／无作品信息，记 no_result；它不证明解析成功、限流或永久不可用。剩余额度内再试其他站点。
3. 返回正确作品但保存失败记 parsed_download_failed。B 站在 WorkBuddy 可先采用经当次验证的“解析站按钮→用户浏览器下载”路径；只用解析站结果，不从原生播放器提取。
4. 有公开文件链接时可由既有工具保存；明确 403 后不重复切代理或伪装头。浏览器下载可作为不同传输动作，沿用原站点同轮；若站点明确要求桌面客户端就改下一站，不安装客户端。
5. 浏览器无事件接口时，只核对本任务点击产生的确切文件名、时间、大小和哈希；未知文件不认领、不清理。不要遍历删除下载目录或依赖未知剪贴板。
成功：实际文件、目标身份、完整性、时长／图序通过；解析成功与取得成功分列，route=parser 且有来源回执。用户导入只能记 user_import，不把尚未发生的导入当成功。
上限：原轮三站；每站有依据的传输恢复一次。相同链接相同拒绝不重复；未决收费请求另按恢复协议，不能重提。
停止／恢复：耗尽或无保存路线就待处理并提供本地导入入口，保留用户原件。
