# DynamoDB Single-Table Model (v0.1)

## Goal (v1.0)

We need query patterns that unblock UI + API **without scans**:

1. List runs (latest first)
2. Get run details + stats
3. List findings for a run (filters later)
4. Get finding details by findingId
5. Get latest PingCastle rules pack + pack metadata

> Constraint: current `template.yaml` creates **only** `pk` (HASH) + `sk` (RANGE), no GSIs.

---

## Partition / Sort key patterns

### 1) RUN (metadata)

- **pk:** `RUN#<runId>`
- **sk:** `META`
- entityType: `RUN`

Attributes (minimum):

- runId, source, domain
- generationDate, generationDateUtc
- rawS3Key, rulesPackId
- findingCount, stats
- schemaVersion

### 2) RUN_INDEX (list runs, latest first)

To list runs efficiently (no scan):

- **pk:** `RUNS#<source>` (ex: `RUNS#pingcastle`)
- **sk:** `<generationDateUtc>#RUN#<runId>` (ISO UTC sorts naturally)
- entityType: `RUN_INDEX`

Query for latest:

Query `pk=RUNS#pingcastle`, `ScanIndexForward=false`, `Limit=1`.

Attributes (minimum):

- runId, source, domain
- generationDate, generationDateUtc
- rawS3Key, rulesPackId
- findingCount, stats
- schemaVersion

Attributes (minimum):

- findingId, runId, source, domain
- asff (full JSON)
- schemaVersion

Attributes (minimum):

- findingId, runId, source, domain
- severityLabel, title
- asff (full JSON)
- schemaVersion

Query findings of a run:

- Query `pk=RUN#<runId>` and `begins_with(sk, "FINDING#")`.

- **pk:** `FINDING#<findingId>`
- **sk:** `META`

Get finding details:

- `GetItem(pk="FINDING#<findingId>", sk="META")`.

- Stores the same `asff` payload as the run-partitioned item (v0.1).

Get finding details:

Rules pack metadata:

- **pk:** `PINGCASTLE#RULES`
- **sk:** `PACK#<packId>`
- entityType: `RULES_PACK`
- Stores metadata only (packId, curatedS3Key, updatedAt, ruleCount, rawS3Key)

Rules pack metadata:

Latest pointer:

- **pk:** `PINGCASTLE#RULES`
- **sk:** `LATEST`
- entityType: `RULES_LATEST`
- Stores packId + curatedS3Key.

- Stores metadata only (packId, curatedS3Key, updatedAt, ruleCount, rawS3Key)

Latest pointer:

Rules pack:

- `curated/pingcastle/rules/packId=<packId>/rules.json`
- `curated/pingcastle/rules/latest.json` (pointer)

- **sk:** `LATEST`

Run snapshot:

- `curated/pingcastle/runs/runId=<runId>/findings.asff.json`

- Stores packId + curatedS3Key.

---

We keep space for:

- Overrides/tags by findingId
- Compliance mappings (riskId → controlId, etc.)
- Compliance reports (runId + frameworkId → coverage/gaps)

Rules pack:

- `curated/pingcastle/rules/packId=<packId>/rules.json`
- `curated/pingcastle/rules/latest.json` (pointer)

Run snapshot:

- `curated/pingcastle/runs/runId=<runId>/findings.asff.json`

---

## Future placeholders (not in v1.0, but reserved)

We keep space for:

- Overrides/tags by findingId
- Compliance mappings (riskId → controlId, etc.)
- Compliance reports (runId + frameworkId → coverage/gaps)

…but we do not add them to v0.1 unless needed by UI wiring.
