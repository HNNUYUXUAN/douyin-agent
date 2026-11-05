---
{
  "type": "Runbook",
  "title": "维护验收：全新设备矩阵",
  "description": "维护验收：全新设备矩阵",
  "tags": [
    "acceptance",
    "maintenance",
    "clean-test"
  ],
  "status": "stable",
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
    "skill": "2.5.1 candidate",
    "host": "Windows x64; recheck current host capabilities"
  },
  "verification_scope": "Candidate implementation; fixture, local and recipient results are recorded separately."
}
---

# 维护验收：全新设备矩阵


## 触发与范围
仅用户明确要求维护验收时读取。普通安装到配置完成即结束，不进入本清单。异机只安装、调试、验收和回传，源码修改及发布由维护设备完成。
## 前置
先完成 setup 并复用有效安装、配置和证据；不要重置设备或重装依赖来制造零装条件。缺 Key 停下等待本地填写。新设备／同机重定位／夹具分别标记。
## 执行
1. 用接受测试的明确范围选择首次、重复、升级、中断恢复及实际存在的终端；不适用项标未测，不额外安装终端。
2. 离线套件：`PYTHON SKILL/scripts/test_all.py --workspace WORKSPACE`。桥接／取源码改动再按仓库 AGENTS 的要求跑对应 PS5/PS7 夹具。
3. 浏览器实际验证：Chrome/Edge 分别可用、指定实例失效、内置实例不进入平台候选、已登录不建登录页、未知／未登录才留两页；不主动结束用户浏览器。
4. Key 缺失仅在隔离夹具制造，不删主工作区 Key。验证保存等待位置、无后续媒体／云请求；填好后复查，setup 收尾而非自动样例。
5. 用户另行开工后才验证作品；模式、范围、用量按已有授权。下载、完整性、理解、原帧复核、清理分别记录，未决请求不重提。
6. 新聊天发现必须由用户实际新开聊天验证。验证者只拿候选目录和普通安装指令，不提供作者历史或预期通过答案；记录宿主和模型版本。
## 成功、上限与交接
每项有时间、证据和范围；原编号问题表直接随提示词提供，不让接收端重建。不能执行的保留 pending。一次受影响回归完成后收尾，不反复跑无变化用例。按普通目录回传，不含凭据、原媒体和私人日志。
