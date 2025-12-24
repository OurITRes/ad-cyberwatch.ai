# AWS Security Finding Format (ASFF) - Minimal Profile

## 1. Purpose / Scope

Ce document définit le profil minimal d’un enregistrement de type "Finding" inspiré du format
AWS Security Finding Format (ASFF), adapté pour l’intégration de sources comme PingCastle et BHE.
Il vise à standardiser la structure des findings pour faciliter leur traitement, leur stockage (ex: DynamoDB) et
leur exploitation dans un contexte multi-source.

## 2. FindingRecord profile v0.1 (ASFF-like)

### 2.1 Champs requis (minimum vital)

- `SchemaVersion` (ex: "2018-10-08")
- `Id` (string unique)
- `ProductArn` (placeholder interne pour l’instant)
- `GeneratorId` (ex: "pingcastle")
- `AwsAccountId` ("000000000000" en POC si non-AWS)
- `Types` (ex: ["Software and Configuration Checks/Industry and Regulatory Standards"])
- `CreatedAt`, `UpdatedAt` (ISO8601)
- `Severity.Label` (INFORMATIONAL | LOW | MEDIUM | HIGH | CRITICAL)
- `Title`
- `Description`
- `Resources[]` (au moins 1 resource, même “domain”)
- `RecordState` (ACTIVE | ARCHIVED)
- `Workflow.Status` (NEW | NOTIFIED | SUPPRESSED | RESOLVED)

### 2.2 Champs optionnels (standardisés)

- `Remediation` (Objet contenant `Recommendation.Text` et `Recommendation.Url`)
- `Compliance` (Objet contenant `Status`, `RelatedRequirements`)
- `ProductFields` (pour extensions internes)
- `UserDefinedFields` (pour extensions internes)

### 2.3 Extensions internes (UserDefinedFields ou ProductFields)

- `source` (pingcastle | bhe)
- `runId`
- `ruleId` (PingCastle)
- `domainFqdn`
- `evidenceS3Key`
- `compliance.links[]` (controlId list)

## 3. ID strategy

L’identifiant `Id` doit être déterministe et unique pour chaque finding. Il est construit à partir de :

- `source` (ex: pingcastle)
- `ruleId` (ou équivalent)
- `asset` (ex: domainFqdn)
- `runId` (identifiant d’exécution)

Exemple :

```text
pingcastle:ruleId=PC-001;domain=labad.local;runId=2024-12-24T10:00:00Z
```

## 4. Severity mapping

| PingCastle Risk | Severity.Label |
|-----------------|----------------|
| 0 (Info)        | INFORMATIONAL  |
| 1 (Low)         | LOW            |
| 2 (Medium)      | MEDIUM         |
| 3 (High)        | HIGH           |
| 4 (Critical)    | CRITICAL       |

## 5. Examples

### 5.1 PingCastle Example 1

```json
{
  "SchemaVersion": "2018-10-08",
  "Id": "pingcastle:ruleId=PC-001;domain=ad_hc_labad.local;runId=2024-12-24T10:00:00Z",
  "ProductArn": "arn:cyberwatch:product/pingcastle",
  "GeneratorId": "pingcastle",
  "AwsAccountId": "000000000000",
  "Types": [
    "Software and Configuration Checks/Industry and Regulatory Standards"
  ],
  "CreatedAt": "2024-12-24T10:00:00Z",
  "UpdatedAt": "2024-12-24T10:00:00Z",
  "Severity": {
    "Label": "HIGH"
  },
  "Title": "Kerberos Pre-Auth Not Required",
  "Description": "Some accounts do not require Kerberos pre-authentication, increasing risk of password attacks.",
  "Resources": [
    {
      "Type": "AwsIamUser",
      "Id": "user1@ad_hc_labad.local",
      "Partition": "aws",
      "Region": "us-east-1"
    }
  ],
  "RecordState": "ACTIVE",
  "Workflow": {
    "Status": "NEW"
  },
  "ProductFields": {
    "source": "pingcastle",
    "runId": "2024-12-24T10:00:00Z",
    "ruleId": "PC-001",
    "domainFqdn": "ad_hc_labad.local",
    "evidenceS3Key": "evidence/PC-001/user1.json",
    "compliance.links": "[\"CIS-1.1.1\"]"
  }
}
```

### 5.2 PingCastle Example 2

```json
{
  "SchemaVersion": "2018-10-08",
  "Id": "pingcastle:ruleId=PC-002;domain=ad_hc_labad.local;runId=2024-12-24T10:00:00Z",
  "ProductArn": "arn:cyberwatch:product/pingcastle",
  "GeneratorId": "pingcastle",
  "AwsAccountId": "000000000000",
  "Types": [
    "Software and Configuration Checks/Best Practices"
  ],
  "CreatedAt": "2024-12-24T10:00:00Z",
  "UpdatedAt": "2024-12-24T10:00:00Z",
  "Severity": {
    "Label": "MEDIUM"
  },
  "Title": "Weak Password Policy",
  "Description": "The domain password policy does not enforce complexity requirements.",
  "Resources": [
    {
      "Type": "Other",
      "Id": "ad_hc_labad.local",
      "Details": {
        "Other": {
          "Type": "AD-Domain"
        }
      }
    }
  ],
  "RecordState": "ACTIVE",
  "Workflow": {
    "Status": "NEW"
  },
  "ProductFields": {
    "source": "pingcastle",
    "runId": "2024-12-24T10:00:00Z",
    "ruleId": "PC-002",
    "domainFqdn": "ad_hc_labad.local",
    "evidenceS3Key": "evidence/PC-002/domain.json",
    "compliance.links": "[\"CIS-1.2.3\"]"
  }
}
```

### 5.3 BHE (BloodHound Enterprise) Example

```json
{
  "SchemaVersion": "2018-10-08",
  "Id": "bhe:ruleId=BHE-001;asset=server01;runId=2024-12-24T10:00:00Z",
  "ProductArn": "arn:cyberwatch:product/bhe",
  "GeneratorId": "bhe",
  "AwsAccountId": "000000000000",
  "Types": [
    "Software and Configuration Checks/Vulnerabilities"
  ],
  "CreatedAt": "2024-12-24T10:00:00Z",
  "UpdatedAt": "2024-12-24T10:00:00Z",
  "Severity": {
    "Label": "LOW"
  },
  "Title": "Unpatched Software Detected",
  "Description": "Server01 is missing critical security updates leading to potential privilege escalation.",
  "Resources": [
    {
      "Type": "Other",
      "Id": "server01.corp.local",
      "Details": {
        "Other": {
          "Type": "AD-Computer",
          "OS": "Windows Server 2019"
        }
      }
    }
  ],
  "RecordState": "ACTIVE",
  "Workflow": {
    "Status": "NEW"
  },
  "ProductFields": {
    "source": "bhe",
    "runId": "2024-12-24T10:00:00Z",
    "ruleId": "BHE-001",
    "evidenceS3Key": "evidence/BHE-001/server01.json",
    "compliance.links": "[\"CUSTOM-1\"]"
  }
}
```

### 5.4 Unmapped finding Example

```json
{
  "SchemaVersion": "2018-10-08",
  "Id": "unmapped:runId=2024-12-24T10:00:00Z",
  "ProductArn": "arn:cyberwatch:product/unmapped",
  "GeneratorId": "custom",
  "AwsAccountId": "000000000000",
  "Types": [
    "Unmapped"
  ],
  "CreatedAt": "2024-12-24T10:00:00Z",
  "UpdatedAt": "2024-12-24T10:00:00Z",
  "Severity": {
    "Label": "INFORMATIONAL"
  },
  "Title": "Unmapped finding",
  "Description": "This finding could not be mapped to a known rule.",
  "Resources": [
    {
      "Type": "Other",
      "Id": "unknown",
      "Details": {
        "Other": {
          "Type": "Unknown"
        }
      }
    }
  ],
  "RecordState": "ACTIVE",
  "Workflow": {
    "Status": "NEW"
  },
  "ProductFields": {
    "source": "custom",
    "runId": "2024-12-24T10:00:00Z"
  }
}
```

---

Document maintenu par l’équipe AD Cyberwatch.ai.
