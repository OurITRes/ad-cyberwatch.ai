# Finding Canonical Model — ASFF-like (v0.1)

## Why ASFF first (v1.0)

For v1.0, **our internal “Unified Weakness Data Model (UDM)” is ASFF-like**:

- **MUST:** AWS Security Finding Format (ASFF) compatibility so our “finding objects” can later be exported to
Security Hub / Security Lake without rewriting the model.
- **SHOULD:** OCSF export (interface-only first).
- **NICE:** ECS export.

ASFF has a clear, stable structure with well-defined required attributes. We adopt an **ASFF minimal profile** (below)
and store the full finding JSON as our canonical record.

> Important: v0.1 is “ASFF-like”, not “we are already sending findings to Security Hub”.
> The goal is: **our internal findings are structurally compatible with ASFF**.

---

## ASFF minimal profile (what we enforce)

### Required top-level attributes (we always populate)

We always populate the required top-level ASFF attributes (per AWS Security Hub docs):

- `SchemaVersion`
- `Id`
- `ProductArn`
- `GeneratorId`
- `AwsAccountId`
- `Types`
- `CreatedAt`
- `UpdatedAt`
- `Severity`
- `Title`
- `Description`
- `Resources`

### Minimal recommended attributes (v0.1)

In addition to the required attributes, we standardize:

- `ProductFields` (**our internal extension point**)  
  - Namespacing rule:
    - `adcyberwatch.*` for internal stable fields
    - `<source>.*` for source-specific fields (`pingcastle.*`, `bhe.*`, …)
- `Remediation.Recommendation.Text` when available (ex: PingCastle rules “Solution”).

---

## Canonical IDs & determinism

### Run ID (PingCastle report)

- `runId` is deterministic, derived from the **report content hash**:
  - `runId = uuid5(namespace, "pingcastle|report|<sha256(report_xml)>")`

### Finding ID (PingCastle)

- One finding per PingCastle `riskId` **per run**:
  - `findingId = uuid5(namespace, "asff|pingcastle|<runId>|<riskId>")`

This ensures:

- Re-ingesting the same file does not create duplicates.
- We can safely re-run ingestion (non-destructive).

---

## Mapping rules (PingCastle)

PingCastle has two XML artifacts:

1) **Rules catalog** (PingCastleRules.xml)  
   - Contains rule definitions (Title/Description/Solution/…)
   - Changes with PingCastle versions

2) **Healthcheck report** (ad_hc_`<domain>`.xml)  
   - Contains the list of detected risks (riskId + points + rationale)  
   - Does **not** contain full rule definitions

v0.1 behavior:

- We ingest the **rules catalog** and store it as a “rules pack”.
- When ingesting a **report**, we enrich findings by joining `riskId` → rule definition from the **latest rules pack**.

---

## Canonical field conventions (ProductFields)

We standardize at least these fields:

### Internal (always)

- `adcyberwatch.source` = `"pingcastle"` | `"bhe"` | …
- `adcyberwatch.runId`
- `adcyberwatch.domain`
- `adcyberwatch.generationDate` (as in source)
- `adcyberwatch.generationDateUtc` (normalized UTC ISO)
- `adcyberwatch.rawS3Key`

### PingCastle specific

- `pingcastle.riskId`
- `pingcastle.category`
- `pingcastle.model`
- `pingcastle.points`
- `pingcastle.rationale`
- `pingcastle.rulesPackId` (rules catalog pack used for enrichment)

---

## Examples (v0.1)

### Example 1 — PingCastle finding (ASFF-like)

```json
{
  "SchemaVersion": "2018-10-08",
  "Id": "adcyberwatch:0f8d3b1b-1c4e-5e2f-b94d-8d1c1b3bb1e2",
  "ProductArn": "arn:aws:securityhub:ca-central-1:123456789012:product/123456789012/default",
  "GeneratorId": "ad-cyberwatch.ai/pingcastle",
  "AwsAccountId": "123456789012",
  "Types": ["Software and Configuration Checks/Vulnerabilities"],
  "CreatedAt": "2025-12-18T19:32:25.687474+00:00",
  "UpdatedAt": "2025-12-18T19:32:25.687474+00:00",
  "Severity": { "Label": "CRITICAL", "Normalized": 90, "Original": "30" },
  "Title": "Mitigate golden ticket attack via a regular change of the krbtgt password",
  "Description": "The purpose is to alert when the password for ...",
  "Resources": [
    {
      "Type": "Other",
      "Id": "ad://domain/labad.local",
      "Partition": "aws",
      "Details": { "Other": { "DomainFQDN": "labad.local" } }
    }
  ],
  "Remediation": {
    "Recommendation": { "Text": "The password of the krbtgt account should be changed..." }
  },
  "ProductFields": {
    "adcyberwatch.source": "pingcastle",
    "adcyberwatch.runId": "<runId>",
    "adcyberwatch.domain": "labad.local",
    "adcyberwatch.generationDate": "2025-12-18T14:32:25.6874739-05:00",
    "adcyberwatch.generationDateUtc": "2025-12-18T19:32:25.687474+00:00",
    "adcyberwatch.rawS3Key": "raw/pingcastle/report/.../ad_hc_labad.local.xml",
    "pingcastle.riskId": "A-Krbtgt",
    "pingcastle.points": "30",
    "pingcastle.rulesPackId": "<packId>"
  }
}
```

### Example 2 — Unmapped finding (placeholder for later sources)

```json
{
  "SchemaVersion": "2018-10-08",
  "Id": "adcyberwatch:<findingId>",
  "ProductArn": "arn:aws:securityhub:ca-central-1:123456789012:product/123456789012/default",
  "GeneratorId": "ad-cyberwatch.ai/<source>",
  "AwsAccountId": "123456789012",
  "Types": ["Uncategorized"],
  "CreatedAt": "2025-12-24T12:00:00+00:00",
  "UpdatedAt": "2025-12-24T12:00:00+00:00",
  "Severity": { "Label": "MEDIUM", "Normalized": 40, "Original": "unknown" },
  "Title": "Source X finding (unmapped)",
  "Description": "Raw finding text...",
  "Resources": [{ "Type": "Other", "Id": "ad://domain/example.local" }],
  "ProductFields": {
    "adcyberwatch.source": "source-x",
    "adcyberwatch.runId": "<runId>"
  }
}
```

---

## Compatibility plan (interfaces only in v1.0)

- **ASFF (MUST):** our canonical record.
- **OCSF (SHOULD):** later export adapter (interface-first).
- **ECS (NICE):** later export adapter.

The “pivot” stays internal and versioned (v0.1 → v0.2 → …), while exports evolve independently.
