# Host acquisition contract / 宿主获取协议

The implementation is capability based: browser, search, local files and media tools. 本机优先宿主连接 Chrome，其他宿主使用对应能力，不要求固定插件或解析网站。

1. Resolve share text/short links in the browser to the canonical video/note URL. Record ID, author, title, caption and reliable source duration or image count/order. 核对作品而非推荐卡片。
2. Read `providers` and prefer verified free parsers for acquisition. Discover candidates using existing search plugins/skills, then host search, then configured Yuanbao/Bocha. Use an available host downloader as the next acquisition route; finally offer user-assisted local import or defer the work. A blob URL is not a downloadable file. 每轮最多三个不同来源，所有尝试计入上限，不自动另开新轮。
3. Submit only a public work URL. No passwords, cookies, keys, paid upgrades or plugin installs. Stop at login/CAPTCHA and record the distinct reason; do not automatically complete a CAPTCHA. 额度耗尽、失效、登录要求、验证码分别登记。
4. Download through supported host capabilities. Record exact paths, SHA256 and whether newly created by this task. For image posts select content images, not recommendation thumbnails; preserve original order and caption. No persistent signed media URLs, page scripts or download tokens.
5. Adopt with acquisition receipt, then check integrity: source identity; duration tolerance max(1 second, 2 video frames); video/audio track presence; full decode; host head/tail inspection. Missing reliable duration means unknown, not complete. Image count/order must match. Whole-file SHA equality can reuse previous head/tail review, explicitly record this basis.
6. Only a passed integrity result can mark a parser successful. Record discovery source URL, service entry, host, steps, support types, last success/failure and failure kind using `providers --receipt FILE`. The local registry is not a portable guarantee. Reverify on another host.

Provider receipt example / 解析来源回执：
```json
{"url":"https://example.org/parse","search_source":"https://example.org","host":"Windows Codex Chrome","instructions":"Paste public URL, inspect identity, download and verify","types":["video"],"outcome":"success","round_id":"host-round-1","job":"ABSOLUTE_JOB_PATH"}
```
Outcome values used by the host: success, failed, quota_exhausted, unavailable, login_required, captcha_required, parsed_download_failed. The last value means parsing succeeded but the file did not land. Source attempts remain in providers history; never treat a successful webpage response as a successful download. Unknown ownership means retain external files, report the gap, and do not sweep Downloads or browser cache. User-assisted imports preserve the original file. Avoid unknown clipboard reads; use explicit download receipts.


## Bulk image ZIP / 图文 ZIP 批量取得

When individual image downloads fail, try another public free parser's bulk ZIP option within the same three-source limit. A parser is a replaceable source, not a required dependency or lasting availability guarantee. A packaging button or success message is not a verified download. Record failed packaging/download attempts as failures; mark a provider successful only after the actual work passes integrity.

逐张图片下载受阻时，可在每轮三个来源的限制内尝试其他公共免费解析站的一键 ZIP。解析站可替换，不是必备依赖，也不保证长期有效。打包按钮或成功提示不证明取得成功；实际打包/下载失败仍登记失败，作品完整性通过才登记成功来源。

Use `PYTHON SKILL/scripts/unpack_images.py --archive ABS_ZIP --workspace ABS_WORKSPACE --output NEW_ABS_DIR --expected-images N`. All paths identify actual locations; output must be a nonexistent short ASCII subdirectory of the workspace. The helper checks archive paths, links/special files, encryption, expansion, expected count and actual decodable image formats before writing normalized images and `manifest.json`. No source archive path is extracted verbatim. Natural filename order is only a candidate order; `order_verified:false` requires host comparison with the original carousel. Pass only those reviewed, ordered image files to adopt.

使用上述命令，输出须为工作区内尚不存在的短 ASCII 子目录。工具在落盘前检查路径、链接/特殊文件、加密、膨胀、数量和可解码图片格式，按实际格式生成图片及 manifest.json，不原样展开 ZIP 内路径。自然文件名排序只是候选顺序，manifest 的 order_verified:false 要由宿主逐张对照原轮播核验；adopt 只接收核验过且按原顺序排列的图片文件。

Acquisition receipts accept `owned_artifacts:[{path:ABS,sha256:HASH,created_by_task:true}]` for task-owned temporary media/ZIPs. Register the ZIP and every extracted task copy with exact hashes so finalize can remove them. `owned_downloads` is still limited to actual adopt media inputs, so a ZIP belongs only in owned_artifacts. These declarations require actual acquisition/ownership proof; never include user originals. Keep the JSON manifest as durable audit text, not an owned media artifact. Finalize cleans registered artifacts after report validation; pre-adopt unregistered downloads require host ownership review and exact-file handling, never directory sweeping.

取得回执新增 owned_artifacts，逐项列 path 绝对路径、sha256、created_by_task:true，用于有取得/所有权证据的临时媒体或 ZIP。登记临时 ZIP 和每张解包副本才能由 finalize 清理；owned_downloads 仍仅限实际 adopt 媒体输入，不能放 ZIP。用户原件不登记，JSON manifest 保留为审计文字。报告验证后 finalize 清理登记文件；adopt 前未登记的下载物须宿主按证据逐文件处理，禁止清空目录。

Copyable commands and receipt construction: [中文取得指南](../docs/agent/zh-CN/acquisition.md) · [English acquisition guide](../docs/agent/en/acquisition.md).
