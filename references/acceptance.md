# v2.3 preparation / 新设备准备 — 2026-11-04

- Added bilingual modular zero-start guides for Windows x64 with only WorkBuddy and its browser connector installed: source acquisition without Git/Python, dependency preparation, host discovery, first task, troubleshooting and clean-device evidence. / 新增中英文分块指引，覆盖无 Git/Python 的源码取得、依赖、宿主发现、首条任务、排错和异机验收。
- Actual PowerShell 5.1, PowerShell 7 and Git Bash installation commands selected WorkBuddy mode and produced `WORKSPACE/.codebuddy/skills/douyin-agent` using an existing isolated QA Conda environment. This tests the installer, not actual WorkBuddy client discovery. / 三个真实终端验证 WorkBuddy 安装目标；复用隔离 QA 环境，不将目录安装当作客户端发现成功。
- 56 offline tests passed (29 runtime, 5 onboarding, 12 installer, 4 ZIP, 6 knowledge/media-tool tests). PowerShell 5.1/7 simulated source downloads verified allowlisted file hashes, preservation of existing destinations and traversal rejection. / 56 项离线测试通过；两个 PowerShell 版本的模拟源码下载通过白名单哈希、已有目录和路径保护检查。
- The public Wiki targets Google OKF 0.2, pinned to official specification commit `62432a095456147ee71e70ac6e4dc0d2dea3ac30`. Eight concepts parsed with a standard YAML parser; init/record/search/reindex/validate used synthetic sanitized evidence. No new runtime dependency or cloud call was added. / Wiki 对齐固定的官方 OKF 0.2 规范；8 个概念经标准 YAML 解析，知识操作用合成脱敏证据验证，未新增运行依赖或云调用。
- WorkBuddy clean-device discovery, actual Chrome/Edge connector execution and a fresh Agent Plan task on another device remain **unverified**. The recipient checklist and template start unverified; only actual device evidence can change them. / WorkBuddy 全新设备发现、其真实浏览器链路和异机新任务仍待验证，不能以本机模拟替代。

---

# v2.2 验收 / Acceptance — 2026-11-03

## Windows terminals and installation / Windows 终端与安装

- Actual Windows PowerShell 5.1, PowerShell 7 and Git Bash each completed first installation, repeat installation, environment preparation, doctor, status and onboard --check. All three produced equal managed-file hashes and equivalent native paths. / 三个真实终端分别完成首次与重复安装、环境准备及三项只读检查；托管文件哈希与路径语义一致。
- A fresh Conda Python 3.12 environment was rebuilt under a workspace path containing spaces, then reused across the terminal checks. Explicit Conda selection, automatic discovery, Git Bash POSIX/Windows paths and PowerShell Set-Location-relative paths passed. / 在含空格路径从锁文件新建独立环境后复用；显式 Conda、自动发现、Git Bash 两类路径和 PowerShell 当前目录相对路径通过。
- 50 offline tests passed: 29 core, 5 onboarding, 4 image-ZIP and 12 installer tests. Installer coverage includes first/repeat install, retirement of hash-matched managed files, preservation of unknown/user-edited files, real Windows sharing locks, partial-write rollback, receipt/context rollback, edits during backup, path traversal and duplicate manifest names. / 50 项离线测试通过，其中安装 12 项覆盖托管文件退役、用户文件保护、真实文件占用、部分写入回滚、回执与上下文恢复、备份期间修改和路径校验。
- Missing Conda was exercised with an invalid explicit executable and an isolated discovery environment; no-D fallback was simulated because this device has D:. Missing keys/tools and read-only behavior were tested offline. / 缺 Conda 用不存在的显式路径及隔离的自动发现环境实测，无 D 盘为模拟；缺 Key、媒体工具和只读行为有离线验证。
- An independent same-machine reader checked public entry routing, CLI help, installer transaction semantics and old 2.0/2.1 receipts. Real cases below are historical v2.1 evidence; this release makes no new cloud calls. / 同机独立读者核验公开入口、CLI、安装事务与旧回执；下方真实案例为 v2.1 历史证据，本轮未新增云请求。

- Actual upgrade from a 2.1 receipt retired 19 hash-matched managed files. Nine existing completed text-only jobs validated successfully through the new entrypoint; private configuration and request-ledger hashes remained unchanged. / 旧 2.1 回执实际升级后移除 19 个哈希匹配的托管文件；新入口成功校验 9 项已有文字结果，私密配置和请求账本哈希保持一致。
- A separate independent reader followed the public branch entry, verified CLI help and all three read-only checks in an empty temporary workspace; the directory remained empty. / 另一独立读者从公开分支入口检查 CLI 与三项只读命令；临时工作区执行后仍为空。

## Publication and scope / 发布与范围

The ordinary release contains 60 allowlisted files, including two heroes and five native Mermaid blocks per README. Relative links, machine-index paths and JSON syntax passed checks. GitCode rendered all five diagrams in each language. In this connected Chrome session, GitHub showed “Unable to render rich display” for both languages; GitHub rendering remains unverified. A 390-pixel viewport check showed GitCode scaling its desktop page, so narrow-screen readers may need zoom or the accompanying text steps. This was browser viewport testing, not a physical phone test. / 普通分发目录包含 60 个白名单文件；每种语言保留一张首图和五张 Mermaid 图。相对链接、索引路径和 JSON 语法通过；GitCode 双语各五图渲染通过；本次连接 Chrome 中 GitHub 双语均显示“Unable to render rich display”，其渲染仍待验证。390 像素视口下 GitCode 缩放桌面页面，窄屏需放大或阅读图后文字；这是浏览器视口测试，非实体手机测试。

Evidence is retained privately under workspace qa/v22. Tests establish Windows same-device installation and relocation. Edge acquisition, another device, other hosts and fresh-chat natural-language discovery remain unverified. / 私有证据保存在工作区 qa/v22；完成 Windows 本机与同机重定位验证，Edge 获取、异机、其他宿主及全新聊天自然语言发现仍待验证。

---

# v2.1 验收 / Acceptance — 2026-11-03

本节记录 v2.1 本轮结果；下方 v2 记录作为历史证据保留，其测试数、作品和调用量不与本轮混合。Windows Codex + 连接 Chrome 已有实测；Edge、异机、其他宿主和全新聊天中的自然语言发现仍待验证。
This section records the v2.1 round. The v2 record below remains historical evidence; its test counts, works and usage are separate. Windows Codex with connected Chrome was exercised. Edge, another device, other hosts and natural-language discovery in a fresh chat remain untested.

## Offline and installation / 离线与安装

- 38 offline tests passed: 29 core (`scripts/test_da.py`), 5 onboarding (`scripts/test_onboarding.py`) and 4 ZIP acquisition (`scripts/test_unpack_images.py`). These tests do not establish live cloud or browser availability. / 38 项离线测试通过：核心 29、首次引导 5、ZIP 获取 4；离线通过不等于浏览器或服务可用。
- Same-device independent environment rebuild under paths containing spaces passed, with ordinary-directory installation, repeat installation, configuration preservation, upgrade and locked-file rollback checks. No credentials were copied. This is not another-device validation. / 同机含空格路径的独立环境重建、普通目录安装、重复安装、配置保留、升级及文件占用回滚已验；未复制凭据，不称为异机验证。
- An independent same-device reader followed Agent entry documents, checked CLI help and read-only doctor/status/onboard, reviewed recovery stop conditions, and exercised synthetic ZIP acquisition and cleanup. A user-import ZIP remained unchanged; registered task copies were removed while text manifests/receipts remained. Synthetic fixtures are not live understanding evidence. / 同机独立读者验证入口、命令、只读检查及恢复停点；合成 ZIP 测试确认用户原件保留、登记副本清理和文字审计留存，合成样本不算真实理解。

## Three live cases / 三类真实案例

| Case / 案例 | Source duration / 源时长 | Visual inputs / 视觉输入 | Requests / 请求数 | Final state / 最终状态 |
|---|---:|---:|---:|---|
| Long video / 长视频 | 506.21678 s | 102 sampled frames / 采样帧 | 22 | completed |
| Short video / 短视频 | 174.375 s | 68 sampled frames / 采样帧 | 15 | completed |
| Image post / 图文 | Not applicable / 不适用 | 9 ordered images / 顺序图片 | 3 | completed |

三例均完成宿主复核及 finalize，清理前后文字校验通过，`cleanup_errors` 为空。长/短视频采用采样视觉理解，不声称逐帧观看。图文逐张下载受阻后经临时 ZIP 取得并核验顺序；登记 ZIP 与解包图片已清理。用户原件保留。请求数和提交量描述该轮处理，不等同于平台结算账单。
All three cases completed host review and finalize. Text validation passed before and after media cleanup, with empty `cleanup_errors`. Video vision was sampled, not every-frame inspection. The image post used a temporary ZIP after individual image downloads were blocked, followed by original-order verification; registered ZIP/extracted images were removed. User originals remain. Request/input counts describe the processing round, not settled platform billing.

Private local evidence: workspace `qa/v21/cases/long-finalize.json`, `short-finalize.json`, `note-finalize.json`, corresponding acquisition/preview records, `qa/v21/install-checks.json`, and `qa/v21/independent-reader.json` plus its Markdown/ZIP evidence. These workspace records, media, credentials and caches are not part of public distribution. / 私有本地证据位于上述工作区相对路径；不随公开仓库交付媒体、凭据、缓存或私人记录。

---

# Historical v2 acceptance / v2 历史验收 — 2026-11-03

Windows Codex 本机验收通过，同机含空格路径环境重建通过；其他宿主、异机和新聊天中的自然语言发现待验证。
Windows Codex local acceptance passed; a new environment rebuilt from the ordinary export under a path with spaces passed. Other hosts/devices and natural-language discovery in a fresh chat remain untested.

- Offline: 26 tests passed, including wrong identity/truncation, real no-audio media, 301-second audio chunking with native offsets (cloud mocked), adaptive sampling, deduplication, image routing, cached recovery after media cleanup, expiry/non-renewal, live locks, orphan process tokens, real Windows exclusive file locks, interrupted cleanup, path tampering, user-original protection, pending reservations, migration and three-provider round limits. No-D/missing-Conda behavior was simulated; this device has D:.
- Same-device relocation: exported ordinary directory, newly rebuilt Python3.12 at a path with spaces, no credentials copied. Final exported-code tests use that environment. This is not an independent-device test.
- Live acquisition: reacquired public video 7581709508896984366, duration484.033333 seconds. Its SHA256 matched the prior fully decoded/host-reviewed file; new full decode passed. Reused a previously verified free public parser via Chrome after the known blob limitation. Reacquired all7 content images for note7300538520215686436 in DOM carousel order. No universal parser availability claim.
- Live understanding: video sampled across9 minute intervals (last partial),126 frames; image post7 images. The complete120-segment native ASR cache was reused. Submitted: 24 Responses requests, 141 image submissions, 0 new audio seconds. There are133 unique submitted images;8 were resubmitted once under the user's continuing authorization after a server-confirmed output-length truncation. Ten completed calls were reused. The original incomplete request remains charged; recovery uses reasoning.effort=low. No automatic retry. Model doubao-seed-2.1-pro. Returned usage is recorded separately from platform billing, which remains unverified.
- Review: host inspected13 actual video frames and all7 image-post images. Confirmed array numbers, red/green partition, l+1==r, the full code template, end card and image order. Corrected the exercise count and image7 statue interpretation. Report distinguishes native ASR misrecognition and visible formula. This is sampled review, not full-frame OCR or full audio listening. Historical travel caption is not current verified advice.
- Lifecycle: reports and review hashes verified before finalize. Task-owned media, registered new browser copies and verified historical copies removed. Durable result/cache/audit files are MD/JSON. User-import original and private .env preserved. Code/environment/config are exempt. Four historical jobs retain human edits/native subtitle timing; ledger submissions, amounts and pending reservations unchanged during migration.
- Packaging: bilingual workflow, MIT original code, dependency-license inventory, unchanged pinned runtime dependencies, setup, source allowlist, installation hashes and code rollback outside skill discovery. Media are excluded from rollback. Ordinary directories only; no archive.

详尽本机证据在工作区 qa/v2；分发目录不携带私人媒体、凭据、缓存或本机取得路径。记录区分本机真实服务、离线模拟和未测宿主，不把安装当服务验证。
Detailed local evidence lives under workspace qa/v2; exports exclude private media, credentials, caches and local acquisition paths. Installation alone does not verify the service.
