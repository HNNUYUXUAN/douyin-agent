---
{
  "type": "Runbook",
  "title": "解析站实测与文件回执",
  "description": "解析站实测与文件回执",
  "tags": [
    "parser",
    "download",
    "解析站",
    "文件回执",
    "bilibili",
    "youtube",
    "xiaohongshu"
  ],
  "status": "active",
  "generated": {
    "by": "douyin-agent/2.5.0",
    "at": "2026-11-05T03:58:14.273533+00:00"
  },
  "sources": [
    {
      "resource": "https://snapany.com/zh/bilibili"
    },
    {
      "resource": "https://snapany.com/zh/tiktok"
    },
    {
      "resource": "https://getfrom.io/en"
    },
    {
      "resource": "https://greenvideo.cc/"
    }
  ],
  "applicability": {
    "skill": "2.5.x",
    "host": "Capabilities rechecked at runtime; measured scope in body"
  }
}
---

# 解析站实测与文件回执

本轮本机为 Windows 11 x64（10.0.26300）、已连接 Chrome 156.0.8078.81、Codex 桌面宿主。宿主及连接扩展版本未知。下表只证明所列公开样本当次通过；新任务仍需实时验证。

| 解析入口 | 本次成功样本 | 文件保存依据 |
|---|---|---|
| https://snapany.com/zh/bilibili | BV1dC4y117Rz 的 p1、BV1Lphuz7E6w 的 p2 | 可见视频链接由宿主下载接口返回确切文件路径，身份、时长、完整解码和首尾通过 |
| 同上 | 动态 792155723808112674，一张长图 | 同一解析结果图片链接在浏览器显示403；设备现有 curl 无 Cookie、无额外请求头取得200，3707×8000 JPEG 校验通过 |
| https://snapany.com/zh/tiktok | 抖音 7574366810088148709 | 公开解析结果文件链接；浏览器保存超时后，现有 curl 取得200，15.8秒文件通过身份、时长与首尾检查 |
| https://getfrom.io/en | YouTube zKYNITx17Mw | 选择720p收到下载事件与路径，6.083628秒文件完整性通过 |
| https://greenvideo.cc/ | 小红书 6aea848900000000030011bf，一张竞赛海报 | 解析站给出的图片链接由现有 curl 保存，2448×3264 JPEG 校验通过 |

## 开工前探测保存能力

先检测宿主下载技能、下载事件／链接保存接口，以及设备已有 curl 等标准文件传输工具。`onboard --check` 的 `curl=true` 只代表命令存在，仍需本轮实际文件回执验证。浏览器缺下载事件不等于整个设备无法保存文件。

标准传输工具仅保存解析站**实际返回的公开文件链接**。确认目标来自正确作品解析结果；使用显式任务输出路径，不从平台播放器、Cookie 或隐藏接口提取链接。不要添加账号 Cookie、私有令牌或为规避拒绝而伪装请求头。只接受实际文件、哈希和完整性检查；网页成功、后台生成完成与文件取得分别记录。临时签名链接使用后清理，不写入公共知识或永久日志。

## 同轮恢复与来源上限

每个作品每轮最多三个不同解析站域名；同站不同路径或不同浏览器不增加额度，也不重置额度。访问前记 attempting；登录墙、验证码、不可用和 parsed_download_failed 均计数。传输方式切换沿用原站点、原 round_id，保留之前失败记录。失败后不开新轮规避上限。

本轮 GreenVideo、Kedou 部分按钮未返回确切路径，不能断言浏览器没有保存任何文件。小红书其他来源出现无实际结果、或站点报告自动访问受限；这只是该样本观察。标为 UI example 的图片不算真实结果。无需再寻找来源即可保存已取得的同轮公开链接。

`providers` 的 previously_verified 仅表示最新成功且 route=parser 的历史；needs_live_validation 始终要求当次核验。旧平台/CDN来源保留可读，作为历史证据。

## 来源发现与清理

已有搜索插件／技能 → 宿主原生搜索 → 已配置元宝／博查；全部不可用时给安装或本地配置引导。取得失败登记待处理并提供 user_import。只清理回执中已证明所有权且哈希一致的任务媒体；未知所有权下载和用户导入原件保留。
