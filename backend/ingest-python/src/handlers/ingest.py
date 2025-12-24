import json
import os
import hashlib
import uuid
from datetime import datetime, timezone
import xml.etree.ElementTree as ET
from urllib.parse import unquote_plus

import boto3

# -----------------------------------------------------------------------------
# ad-cyberwatch.ai — PingCastle ingestion (v0.1)
#
# This Lambda is triggered by S3 ObjectCreated events on RawBucket (via EventBridge).
# It supports TWO PingCastle XML artifacts:
#   1) Rules catalog (PingCastleRules.xml)  -> curated/pingcastle/rules/... + DDB metadata
#   2) Healthcheck report (ad_hc_<domain>.xml) -> ASFF-like findings + RUN summary in DDB
#
# Non-destructive principle:
# - We never delete raw objects.
# - Curated outputs are written under content-hash derived keys (packId/runId) so re-uploads
#   remain deterministic.
# -----------------------------------------------------------------------------

s3 = boto3.client("s3")
ddb = boto3.resource("dynamodb")

MAIN_TABLE_NAME = os.environ.get("MAIN_TABLE_NAME")
CURATED_BUCKET = os.environ.get("CURATED_BUCKET")

table = ddb.Table(MAIN_TABLE_NAME)

ASFF_SCHEMA_VERSION = "2018-10-08"

# Stable namespace UUID for deterministic uuid5 IDs.
NAMESPACE_UUID = uuid.UUID("b2c3d6ea-4f79-4b9b-9c9b-4d6a0f2d0d6a")


def handler(event, context):
    print(f"Event received: {json.dumps(event)}")

    bucket, key = _extract_s3_bucket_key(event)
    if not bucket or not key:
        return {"statusCode": 400, "body": json.dumps({"message": "Bad event structure"})}

    print(f"Processing: s3://{bucket}/{key}")

    obj = s3.get_object(Bucket=bucket, Key=key)
    raw_bytes = obj["Body"].read()
    xml_text = raw_bytes.decode("utf-8", errors="replace")

    # Parse XML once, then detect artifact type from root structure.
    try:
        root = ET.fromstring(xml_text)
    except ET.ParseError:
        print("Not valid XML -> ignoring")
        return {"statusCode": 204, "body": json.dumps({"message": "Not XML"})}

    # PingCastle XML typically has no namespaces, but be defensive:
    _strip_namespaces_inplace(root)

    artifact_type = detect_pingcastle_artifact(root)

    if artifact_type == "rules":
        return process_rules_catalog(root, xml_text, key)

    if artifact_type == "report":
        return process_report(root, xml_text, key, context)

    print("Unknown PingCastle artifact -> ignoring")
    return {"statusCode": 204, "body": json.dumps({"message": "Unknown artifact"})}


# -----------------------------------------------------------------------------
# Event helpers
# -----------------------------------------------------------------------------

def _extract_s3_bucket_key(event: dict):
    """
    Supports:
    - EventBridge S3 events: event.detail.bucket.name + event.detail.object.key
    - S3 Notifications: event.Records[].s3.bucket.name + event.Records[].s3.object.key

    Note: keys can be URL-encoded, so we decode via unquote_plus.
    """
    # EventBridge
    if isinstance(event, dict) and "detail" in event:
        d = event["detail"]
        return d["bucket"]["name"], unquote_plus(d["object"]["key"])

    # S3 notification
    if isinstance(event, dict) and "Records" in event:
        for r in event.get("Records", []):
            if "s3" in r:
                return r["s3"]["bucket"]["name"], unquote_plus(r["s3"]["object"]["key"])

    return None, None


def utc_now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()


def sha256_hex_str(s: str) -> str:
    return hashlib.sha256(s.encode("utf-8")).hexdigest()


def normalize_domain(domain: str) -> str:
    return (domain or "unknown").lower().rstrip(".")


def get_account_region_from_context(context):
    arn = getattr(context, "invoked_function_arn", "") or ""
    parts = arn.split(":")
    region = parts[3] if len(parts) > 3 else (os.environ.get("AWS_REGION") or "ca-central-1")
    account = parts[4] if len(parts) > 4 else "000000000000"
    return account, region


def parse_iso_to_utc_iso(dt_str: str) -> str:
    """
    PingCastle GenerationDate example: 2025-12-18T14:32:25.6874739-05:00

    We normalize to UTC ISO for:
    - Run ordering (DDB run index)
    - Consistent timestamps
    """
    if not dt_str:
        return utc_now_iso()
    try:
        # Python can't parse 7-digit fractional seconds -> trim to 6.
        # Keep timezone offset.
        m = dt_str
        if "." in m:
            head, tail = m.split(".", 1)
            frac = "".join(ch for ch in tail if ch.isdigit())
            tz = tail[len(frac):]
            frac = (frac + "000000")[:6]
            m = f"{head}.{frac}{tz}"
        dt = datetime.fromisoformat(m)
        if dt.tzinfo is None:
            dt = dt.replace(tzinfo=timezone.utc)
        return dt.astimezone(timezone.utc).isoformat()
    except Exception:
        return utc_now_iso()


def _strip_namespaces_inplace(root: ET.Element):
    """
    Remove {namespace} prefixes so XPath searches remain stable.
    """
    for el in root.iter():
        if "}" in el.tag:
            el.tag = el.tag.split("}", 1)[1]


# -----------------------------------------------------------------------------
# Artifact detection
# -----------------------------------------------------------------------------

def detect_pingcastle_artifact(root: ET.Element) -> str:
    # Rules catalog
    if root.tag == "ArrayOfExportedRule" or root.find("ExportedRule") is not None:
        return "rules"

    # Healthcheck report
    if root.find(".//RiskRules") is not None and root.find(".//DomainFQDN") is not None:
        return "report"

    return "unknown"


# -----------------------------------------------------------------------------
# Rules catalog processing
# -----------------------------------------------------------------------------

def process_rules_catalog(root: ET.Element, xml_text: str, raw_s3_key: str):
    """
    Stores:
    - S3 curated pack (content-hash keyed)
    - S3 curated "latest" pointer
    - DDB pack metadata + DDB latest pointer

    Note: We do NOT store all rules in DDB to avoid large items.
    """
    rules_by_riskid = parse_rules_catalog(root)

    pack_id = sha256_hex_str(xml_text)
    ingested_at = utc_now_iso()

    curated_key = f"curated/pingcastle/rules/packId={pack_id}/rules.json"
    latest_key = "curated/pingcastle/rules/latest.json"

    payload = {
        "packId": pack_id,
        "source": "pingcastle",
        "artifactType": "rules",
        "ingestedAt": ingested_at,
        "rawS3Key": raw_s3_key,
        "ruleCount": len(rules_by_riskid),
        "rulesByRiskId": rules_by_riskid,
        "schemaVersion": "v0.1",
    }

    # Write pack JSON
    s3.put_object(
        Bucket=CURATED_BUCKET,
        Key=curated_key,
        Body=json.dumps(payload, indent=2),
        ContentType="application/json",
    )

    # Write "latest pointer"
    latest_payload = {
        "packId": pack_id,
        "curatedS3Key": curated_key,
        "updatedAt": ingested_at,
        "ruleCount": len(rules_by_riskid),
        "schemaVersion": "v0.1",
    }
    s3.put_object(
        Bucket=CURATED_BUCKET,
        Key=latest_key,
        Body=json.dumps(latest_payload, indent=2),
        ContentType="application/json",
    )

    # DDB metadata + latest
    table.put_item(
        Item={
            "pk": "PINGCASTLE#RULES",
            "sk": f"PACK#{pack_id}",
            "entityType": "RULES_PACK",
            "packId": pack_id,
            "curatedS3Key": curated_key,
            "updatedAt": ingested_at,
            "ruleCount": len(rules_by_riskid),
            "rawS3Key": raw_s3_key,
            "schemaVersion": "v0.1",
        }
    )
    table.put_item(
        Item={
            "pk": "PINGCASTLE#RULES",
            "sk": "LATEST",
            "entityType": "RULES_LATEST",
            "packId": pack_id,
            "curatedS3Key": curated_key,
            "updatedAt": ingested_at,
            "ruleCount": len(rules_by_riskid),
            "schemaVersion": "v0.1",
        }
    )

    print(f"Rules catalog processed. packId={pack_id}")
    return {"statusCode": 200, "body": json.dumps({"message": "Rules catalog processed", "packId": pack_id})}


def parse_rules_catalog(root: ET.Element) -> dict:
    out = {}
    for r in root.findall("ExportedRule"):
        risk_id = _get_text(r, "RiskId")
        if not risk_id:
            continue

        out[risk_id] = {
            "riskId": risk_id,
            "title": _get_text(r, "Title"),
            "description": _get_text(r, "Description"),
            "solution": _get_text(r, "Solution"),
            "documentation": _get_text(r, "Documentation"),
            "technicalExplanation": _get_text(r, "TechnicalExplanation"),
            "category": _get_text(r, "Category"),
            "model": _get_text(r, "Model"),
            "type": _get_text(r, "Type"),
            "maturityLevel": _get_text(r, "MaturityLevel"),
        }
    return out


# -----------------------------------------------------------------------------
# Report processing
# -----------------------------------------------------------------------------

def process_report(root: ET.Element, xml_text: str, raw_s3_key: str, context):
    generation_date = _find_text(root, ".//GenerationDate") or utc_now_iso()
    generation_date_utc = parse_iso_to_utc_iso(generation_date)
    domain = normalize_domain(_find_text(root, ".//DomainFQDN") or "unknown")

    # Deterministic runId from content hash
    report_hash = sha256_hex_str(xml_text)
    run_id = str(uuid.uuid5(NAMESPACE_UUID, f"pingcastle|report|{report_hash}"))

    # Load latest rules pack (optional but recommended)
    rules_pack_id, rules_by_riskid = load_latest_rules_pack()

    # Parse RiskRules
    risk_rules = root.find(".//RiskRules")
    parsed = []
    if risk_rules is not None:
        for rr in risk_rules.findall("HealthcheckRiskRule"):
            risk_id = _get_text(rr, "RiskId")
            if not risk_id:
                continue
            parsed.append(
                {
                    "riskId": risk_id,
                    "category": _get_text(rr, "Category"),
                    "model": _get_text(rr, "Model"),
                    "points": _get_text(rr, "Points"),
                    "rationale": _get_text(rr, "Rationale"),
                }
            )

    if not parsed:
        print("No RiskRules found -> no findings")
        return {"statusCode": 204, "body": json.dumps({"message": "No findings"})}

    account, region = get_account_region_from_context(context)

    # For now we keep a SecurityHub-like ProductArn to stay aligned with ASFF.
    product_arn = f"arn:aws:securityhub:{region}:{account}:product/{account}/default"

    created_at = generation_date_utc
    updated_at = created_at

    # Build ASFF findings + DDB items
    findings_items = []
    index_items = []

    stats = {"CRITICAL": 0, "HIGH": 0, "MEDIUM": 0, "LOW": 0, "INFORMATIONAL": 0}

    for f in parsed:
        risk_id = f["riskId"]
        rule_def = rules_by_riskid.get(risk_id, {})

        sev_label, sev_norm = pingcastle_points_to_asff_sev(f.get("points", ""))

        stats[sev_label] = stats.get(sev_label, 0) + 1

        finding_id = str(uuid.uuid5(NAMESPACE_UUID, f"asff|pingcastle|{run_id}|{risk_id}"))

        title = rule_def.get("title") or f"PingCastle {risk_id}"
        description = rule_def.get("description") or f.get("rationale") or ""

        remediation_text = rule_def.get("solution") or ""

        # --- Minimal ASFF profile (see docs/schema/finding-asff-v0.1.md) ---
        asff = {
            "SchemaVersion": ASFF_SCHEMA_VERSION,
            "Id": f"adcyberwatch:{finding_id}",
            "ProductArn": product_arn,
            "GeneratorId": "ad-cyberwatch.ai/pingcastle",
            "AwsAccountId": account,
            "Types": ["Software and Configuration Checks/Vulnerabilities"],
            "CreatedAt": created_at,
            "UpdatedAt": updated_at,
            "Severity": {
                "Label": sev_label,
                "Normalized": sev_norm,
                "Original": str(f.get("points", "")),
            },
            "Title": title,
            "Description": description,
            "Resources": [
                {
                    "Type": "Other",
                    "Id": f"ad://domain/{domain}",
                    "Partition": "aws",
                    "Details": {"Other": {"DomainFQDN": domain}},
                }
            ],
            "ProductFields": {
                # Internal stable fields (namespaced)
                "adcyberwatch.source": "pingcastle",
                "adcyberwatch.runId": run_id,
                "adcyberwatch.domain": domain,
                "adcyberwatch.generationDate": generation_date,
                "adcyberwatch.generationDateUtc": generation_date_utc,
                "adcyberwatch.rawS3Key": raw_s3_key,
                # PingCastle specific
                "pingcastle.riskId": risk_id,
                "pingcastle.category": f.get("category", ""),
                "pingcastle.model": f.get("model", ""),
                "pingcastle.points": str(f.get("points", "")),
                "pingcastle.rationale": f.get("rationale", ""),
                "pingcastle.rulesPackId": rules_pack_id or "",
            },
        }

        if remediation_text:
            asff["Remediation"] = {"Recommendation": {"Text": remediation_text}}

        # DDB items
        findings_items.append(
            {
                "pk": f"RUN#{run_id}",
                "sk": f"FINDING#{finding_id}",
                "entityType": "FINDING",
                "runId": run_id,
                "findingId": finding_id,
                "source": "pingcastle",
                "domain": domain,
                "riskId": risk_id,
                "severityLabel": sev_label,
                "title": title,
                "asff": asff,
                "schemaVersion": "v0.1",
            }
        )
        index_items.append(
            {
                "pk": f"FINDING#{finding_id}",
                "sk": "META",
                "entityType": "FINDING_INDEX",
                "runId": run_id,
                "findingId": finding_id,
                "source": "pingcastle",
                "domain": domain,
                "riskId": risk_id,
                "severityLabel": sev_label,
                "title": title,
                "asff": asff,
                "schemaVersion": "v0.1",
            }
        )

    # RUN summary
    run_item = {
        "pk": f"RUN#{run_id}",
        "sk": "META",
        "entityType": "RUN",
        "runId": run_id,
        "source": "pingcastle",
        "domain": domain,
        "generationDate": generation_date,
        "generationDateUtc": generation_date_utc,
        "createdAt": created_at,
        "rawS3Key": raw_s3_key,
        "rulesPackId": rules_pack_id or "",
        "findingCount": len(findings_items),
        "stats": stats,
        "schemaVersion": "v0.1",
    }

    # RUN index for list/latest queries without a table scan
    run_index_item = {
        "pk": "RUNS#pingcastle",
        "sk": f"{generation_date_utc}#RUN#{run_id}",
        "entityType": "RUN_INDEX",
        "runId": run_id,
        "source": "pingcastle",
        "domain": domain,
        "generationDateUtc": generation_date_utc,
        "generationDate": generation_date,
        "findingCount": len(findings_items),
        "schemaVersion": "v0.1",
    }

    # Write to DDB (batch)
    with table.batch_writer(overwrite_by_pkeys=["pk", "sk"]) as batch:
        batch.put_item(Item=run_item)
        batch.put_item(Item=run_index_item)
        for it in findings_items:
            batch.put_item(Item=it)
        for it in index_items:
            batch.put_item(Item=it)

    # Write curated snapshot (ASFF list)
    curated_key = f"curated/pingcastle/runs/runId={run_id}/findings.asff.json"
    s3.put_object(
        Bucket=CURATED_BUCKET,
        Key=curated_key,
        Body=json.dumps(
            {
                "runId": run_id,
                "source": "pingcastle",
                "domain": domain,
                "generationDate": generation_date,
                "generationDateUtc": generation_date_utc,
                "rawS3Key": raw_s3_key,
                "rulesPackId": rules_pack_id or "",
                "findingCount": len(findings_items),
                "stats": stats,
                "findings": [it["asff"] for it in findings_items],
                "schemaVersion": "v0.1",
            },
            indent=2,
        ),
        ContentType="application/json",
    )

    print(f"Report processed. runId={run_id}, findings={len(findings_items)}")
    return {"statusCode": 200, "body": json.dumps({"message": "Report processed", "runId": run_id})}


def load_latest_rules_pack():
    """
    Loads the latest rules pack pointer from DDB, then loads the pack payload from S3 curated.
    If missing, we still ingest reports (but we lose Title/Description/Solution enrichment).
    """
    try:
        resp = table.get_item(Key={"pk": "PINGCASTLE#RULES", "sk": "LATEST"})
        item = resp.get("Item")
        if not item:
            print("No LATEST rules pack in DDB.")
            return None, {}

        pack_id = item.get("packId")
        curated_s3_key = item.get("curatedS3Key")
        if not curated_s3_key:
            return pack_id, {}

        obj = s3.get_object(Bucket=CURATED_BUCKET, Key=curated_s3_key)
        payload = json.loads(obj["Body"].read().decode("utf-8"))
        return pack_id, payload.get("rulesByRiskId", {}) or {}
    except Exception as e:
        print(f"Failed to load latest rules pack: {str(e)}")
        return None, {}


def pingcastle_points_to_asff_sev(points_str: str):
    """
    Current heuristic (can be tuned later):
    - >=30 -> CRITICAL
    - >=20 -> HIGH
    - >=10 -> MEDIUM
    - >=1  -> LOW
    - 0    -> INFORMATIONAL
    """
    try:
        p = int(points_str)
    except Exception:
        p = 0

    if p >= 30:
        return "CRITICAL", 90
    if p >= 20:
        return "HIGH", 70
    if p >= 10:
        return "MEDIUM", 40
    if p >= 1:
        return "LOW", 20
    return "INFORMATIONAL", 0


def _get_text(parent: ET.Element, tag: str) -> str:
    e = parent.find(tag)
    return e.text.strip() if e is not None and e.text else ""


def _find_text(root: ET.Element, path: str) -> str:
    e = root.find(path)
    return e.text.strip() if e is not None and e.text else ""
