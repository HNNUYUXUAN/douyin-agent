---
{
  "type": "Runbook",
  "title": "Knowledge retrieval and recording",
  "description": "Knowledge retrieval and recording — douyin-agent operational knowledge",
  "tags": [
    "douyin-agent",
    "en",
    "bootstrap",
    "knowledge"
  ],
  "status": "active",
  "generated": {
    "by": "douyin-agent/2.5.0",
    "at": "2026-11-05T02:27:48.555869+00:00"
  },
  "sources": [
    {
      "resource": "https://github.com/GoogleCloudPlatform/knowledge-catalog/blob/62432a095456147ee71e70ac6e4dc0d2dea3ac30/okf/SPEC.md"
    }
  ],
  "applicability": {
    "skill": "2.5.x",
    "host": "capability-detected; see body for measured versions"
  },
  "verification_scope": "Documentation reviewed; runtime acceptance is recorded separately."
}
---

# Knowledge retrieval and recording

The public [wiki/index.md](../../index.md) is a Google OKF 0.2 knowledge bundle of installation, host and recovery concepts; [pinned specification](https://github.com/GoogleCloudPlatform/knowledge-catalog/blob/62432a095456147ee71e70ac6e4dc0d2dea3ac30/okf/SPEC.md). Concepts use Markdown plus YAML frontmatter and path identity; reserved index.md/log.md provide navigation/history. The writer uses JSON mappings, a valid YAML subset, without an added YAML dependency.

The public Wiki is distributed with releases; private cases live in workspace `knowledge-private/`. Search/validate are read-only; init/reindex/record write files. Retrieval is keyword-based and needs no vector database, extra key or Google account. Hosts are not assumed to discover the Wiki automatically: SKILL.md and the Agent index explicitly link it.

```text
PYTHON SKILL/scripts/knowledge.py --workspace WORKSPACE search --query "WorkBuddy browser connection"
PYTHON SKILL/scripts/knowledge.py --workspace WORKSPACE init
PYTHON SKILL/scripts/knowledge.py --workspace WORKSPACE record --file CASE_JSON
PYTHON SKILL/scripts/knowledge.py --workspace WORKSPACE validate
```

Search public concepts and local cases, then inspect live status, relevant guides and actual errors. Results include public/private scope and paths; historical success is not current health. After remediation, record symptoms, actions, actual results, verification and keywords as JSON; see the [sanitized example](../../../docs/agent/examples/case.json). Sources must be clean public HTTPS URLs or existing workspace-relative MD/JSON evidence. Exclude keys, cookies, signed URLs, absolute machine paths, private transcripts, accounts and original media. Pattern checks are limited; the host still reviews sanitization before writing.

record requires a new ASCII id and never overwrites a case. Use a new revision id and mention the old case when updating. New cases remain draft, without an automatic human-review claim. Rebuild indexes/logs with reindex after interruption. Runtime evidence and unresolved ledgers remain authoritative. Private cases are never automatically uploaded or distributed; publishing a generalized lesson requires separate sanitized review.

A local source such as `workspace:qa/evidence.json` is a project convention: resolve the MD/JSON relative to the current workspace after relocation. It is not a public URL. Generic consumers should preserve unknown URIs and resolve them against the actual workspace rather than fetching them remotely.
