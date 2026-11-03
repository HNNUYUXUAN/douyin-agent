# Maintained diagrams / 可维护图解

`diagram-source.json` contains bilingual labels, node positions, edge directions and the palette. `render_diagrams.py` creates the four public PNGs with Pillow; it does not call a model or execute the skill.

```text
python docs/render_diagrams.py
```

Use Python with Pillow 10 or newer. The renderer discovers Microsoft YaHei on Windows and Noto Sans CJK on Linux. For another system, pass paths to existing CJK-capable fonts with `--font PATH --bold-font PATH`; no font is downloaded or bundled. Font choice can change line wrapping, so review all outputs after rendering. The renderer reports text overflow and exits unsuccessfully if it finds any.

- `workflow-zh.png` / `workflow-en.png`: install, onboarding, work verification, paid-request preview, segment analysis, review, finalize, retention and recovery.
- `system-zh.png` / `system-en.png`: the user, Codex host, connected browser, local CLI/workspace, Agent Plan, public sources, durable text and temporary media.

中文与英文采用相同布局及节点关系，文字来自同一 JSON。修改实现后，对照安装指南、Agent 首次使用/任务流程和恢复说明更新图源，再渲染并逐张检查。生成图是系统说明，不是产品截图或性能证据。PNG 为不透明米白底，便于深浅色页面使用；在 README 中保留图片原尺寸链接，供小屏放大阅读。

Source basis: `AGENT_INSTALL.md`, `SKILL.md`, `docs/agent/zh-CN/onboarding.md`, `docs/agent/zh-CN/workflow.md`, `references/recovery.md`, and `scripts/da.py`. No third-party logos or media are included. The original diagram source and renderer follow the repository license. Runtime dependencies and system fonts retain their own licenses.
