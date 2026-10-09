# System architecture — logical view

Status: **Proposed architecture**; not a frozen deployment design.

## Context

~~~mermaid
flowchart LR
  PM["PM / Product"] --> DOCS["Approved business knowledge\nConfluence / requirements"]
  QA["QA"] --> CAPTURE["Browser capture surface\nextension or approved alternative"]
  CAPTURE --> SVC["QA Assistant service"]
  DOCS -. "Scoped read" .-> SVC
  REPO["GitHub / GitLab\nsource & ownership"] -. "Scoped read" .-> SVC
  LOGS["Logs / distributed traces\nfuture integration"] -. "Scoped read" .-> SVC
  SVC --> MODEL["AI runtime adapter\nprovider TBD"]
  MODEL --> SVC
  SVC --> REVIEW["QA review UI\nfact + draft + linked evidence"]
  REVIEW -->|"Approved"| SVC
  SVC -->|"Create / update via API"| JIRA["Jira"]
  JIRA --> DEV["Developer / Coding Agent"]
  DEV --> QA
~~~

**Conceptual, not necessarily separate services.** The QA Assistant service can initially be a small API plus background worker sharing a database. The AI runtime adapter denotes an authorized, programmable model inference interface, **not** a consumer coding-plan subscription by assumption.

## Component responsibilities

| Component | Deterministic responsibilities | AI responsibilities |
| --- | --- | --- |
| Capture surface | Collect action steps, errors, network metadata, screenshots, explicit QA note | None required |
| Intake + evidence storage | Validate, redact, quota, index, retain, link | None required |
| Context resolver | Resolve environment → repository candidates and authoritative documents | Select relevance; explain disagreements |
| Diagnosis worker | Trigger, retries, structured output checks, citations and provenance | Classify symptom, fault domain, hypothesis, missing evidence |
| Review + Jira | Permission, approvals, attachment references, API calls, status | Generate human-readable narrative / suggested routing |
| Observability adapters | Query by request/trace id with least privileges | Interpret retrieved failure signals |

## Deliberate simplifications

- QA/Staging maps to **candidate source branch** for initial code investigation. The branch is **not proof of the deployed build**; an exact build/commit reference is added only if field evidence demonstrates branch drift to be material.
- No requirement for QA to clone the repositories.
- No independent microservice for each logical module.
- Do not mirror all business knowledge into this public repository. Read scoped authoritative docs when needed; evaluate controlled structured copies later.
- No broad backend investigation in v0.1 before logs/trace owners and permissions are understood.

## Runtime processing — conceptual

~~~mermaid
flowchart TB
  IN["Receive observation + evidence"] --> VALIDATE["Validate and redact"]
  VALIDATE --> STORE["Persist evidence / metadata"]
  STORE --> JOB["Queue or background job"]
  JOB --> RULES["Retrieve targeted AC / business rules"]
  JOB --> CODE["Retrieve targeted frontend source"]
  JOB --> OPTIONAL["Optional logs & traces (later)"]
  RULES --> AI["Model reasoning with typed evidence"]
  CODE --> AI
  OPTIONAL --> AI
  AI --> REPORT["Validated diagnosis + Jira draft"]
  REPORT --> QA["QA review"]
  QA -->|Edit / approve| JIRA["Jira API"]
  QA -->|Needs clarification| RECAPTURE["Supplement evidence / correct expectation"]
  RECAPTURE --> JOB
~~~

## Cross-team questions still open

- Which Chrome integration supports required capture without disrupting debugging or violating browser policy?
- What safe model runtime can the service actually call, under which data-processing agreements and cost limits?
- What internal document, source and telemetry systems are available and authorized?
- What Jira fields, workflow transitions and team ownership mappings are authoritative?
- What is the appropriate evidence retention policy and sensitive-data boundary?

See [evidence pipeline](evidence-diagnosis-pipeline.md), [module ownership](module-map.md) and [technical spike](../validation/qa-capture-spike.md).
