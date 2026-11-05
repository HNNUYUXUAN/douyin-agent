---
{
  "type": "Runbook",
  "title": "依赖与解析文件传输",
  "description": "依赖与解析文件传输",
  "tags": [
    "douyin-agent",
    "zh-CN",
    "transfer",
    "v251-runtime"
  ],
  "status": "active",
  "generated": {
    "by": "douyin-agent/2.5.1",
    "at": "2026-11-05T15:06:20.335700+00:00"
  },
  "sources": [
    {
      "resource": "https://requests.readthedocs.io/en/latest/user/quickstart/#timeouts"
    },
    {
      "resource": "../../shared/acceptance/runfix-v251.md"
    }
  ],
  "applicability": {
    "skill": "2.5.1 candidate",
    "host": "Capability-detected; local and recipient evidence separate"
  },
  "verification_scope": "Implementation and offline fixtures; live scope is listed in acceptance evidence."
}
---

# 依赖与解析文件传输

触发：依赖低速／TLS 失败、解析结果可见但保存失败、错误页伪装媒体或暂存积累。适用 v2.5.1 候选，先核对原来源回执与当前轮次。

`da.py --workspace WORKSPACE providers --platform douyin` 返回登记的准确入口；抖音 SnapAny 为 `/zh/tiktok`，不能按平台名拼接路径。先复用已验证免费站，失效按现有检索技能→宿主搜索→已配置元宝／博查发现。每作品每轮最多三个不同站，进入前 attempting，验证码／登录墙／失败计数，同站换传输保留同轮。第一站失败继续剩余来源。

回执用 UTF-8（接受 BOM），通过 `providers --receipt FILE.json` 或 `providers --batch ARRAY.json` 保存；批量全部校验后才提交，可中断重放。attempt_id 由首次记录生成，后续同来源同轮沿用。实际文件采用 adopt，route=parser 且关联来源；完整性通过自动推进 success。传输失败记 parsed_download_failed；无作品结果记 no_result；明确不支持记 failed。收尾显示 attempting，不能据未收口记录宣称完成。

只保存解析站返回的文件，不从平台接口取流。既有浏览器／下载技能负责保存。需要 curl 时运行 `PYTHON SKILL/scripts/transfer.py --workspace WORKSPACE save --url-stdin --provider-receipt SOURCE.json --output out/file.mp4 --kind video`，将当前实际 HTTPS 文件 URL 通过标准输入交付；不提供 Cookie、自定义 UA 或 Referer。先临时落地，再验证大小、类型、SHA256、完整解码，成功才发布目标名。403 错误体不会成为成功 mp4；明确拒绝不重复切代理。传输回执在 out/transfers，成功后自动清理已登记分段；明确结束用 `... cleanup --id ID` 核对哈希清理其他暂存，保留文字回执。修改过的文件保留。

尚无 Python 的 Windows 依赖传输：
```text
powershell.exe -NoProfile -File SKILL/scripts/download-dependency.ps1 -Workspace WORKSPACE -Url OFFICIAL_URL -Output out/dependency.exe -Sha256 EXPECTED_SHA256
```
只接受已登记官方构建来源与完整 SHA256。整包持续低速／超时后最多 8 段，验证 206、Content-Range、各段长度、同一 ETag／Last-Modified，只补失败段一次，合并后核对整包 SHA256；不混来源／版本，TLS 校验保持开启。收到官方错误状态不无限重试。不支持 Range／资源变化／哈希不符则保留诊断停止。用同脚本 `-Cleanup -Workspace WORKSPACE -Output TRANSFER_ID` 清理已核验任务文件；先完成安装与独立可用性核验，不清理环境或源码。

成功：完整文件及来源／身份／时长或图序证据均通过；依赖还须版本、签名检查。上限：原轮三站，失败分段一次；受阻保留待处理及用户本地文件导入入口。网络慢、间歇失败和访问限制分别记录，单次短超时不证明永久不可达。
