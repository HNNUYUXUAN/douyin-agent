# 故障路由索引

先查代码／现象，完整读对应手册再操作。表中的历史编号可直接用 knowledge.py route 检索。

| Code / 编号 | 现象／范围 | 手册 |
|---|---|---|
| install | 安装、终端与源码故障 | [read](install.md) |
| conda | Conda 校验、安装等待与残留 | [read](conda.md) |
| page-controls | 页面初始化、输入与滚动恢复 | [read](page-controls.md) |
| acquisition | 解析、无结果与文件取得故障 | [read](acquisition.md) |
| records | 观察、知识与会话回执故障 | [read](records.md) |
| media | 媒体身份、采样与清理故障 | [read](media.md) |
| unknown | 手册未覆盖故障的有限诊断 | [read](unknown.md) |
| browser.* / F241-4 / O-1,O-3 | Chrome/Edge, login | [read](../operations/browser-selection.md) |
| browser.extension_offline / browser.screenshot_timeout | Bridge / capture | [read](../operations/browser-recovery.md) |
| key.missing / O-4 | Key | [read](../bootstrap/key.md) |
| O-5 | setup | [read](../bootstrap/first-run.md) |

## 精确查询与停止

`PYTHON SKILL/scripts/knowledge.py --workspace WORKSPACE route --code browser.scroll_timeout --language zh-CN`

42 项原编号映射见 [字段回传归档](../../shared/acceptance/field-v251.md)。无匹配才按 unknown：最多一轮官方检索、三个一手来源、两个不同诊断动作；不重复同输入失败，不自动另开一轮。
