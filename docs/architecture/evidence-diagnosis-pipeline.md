# Browser evidence → AI → QA review → Jira

Status: **Proposed technical contract for validation**, not implemented.

## Core decision

The browser extension **does not directly call a model**. It sends a typed, bounded observation plus redacted runtime evidence to a controlled ingestion API. A service performs validation, secure storage, scoped context lookup, model invocation through a legitimate API/runtime, report validation and Jira publication after QA approval.

A browser extension is a candidate entry point, not guaranteed to be the best Chrome capture integration.

~~~mermaid
sequenceDiagram
  actor QA
  participant Browser as Chrome capture
  participant API as QA Assistant API
  participant Store as Evidence store
  participant Worker as Analysis worker
  participant Context as Business/Code tools
  participant AI as Approved AI runtime
  participant Review as QA review UI
  participant Jira as Jira API
  QA->>Browser: Start capture; reproduce; describe
  Browser->>API: POST observation + bounded evidence
  API->>API: Validate, redact, authorize
  API->>Store: Store artifacts and references
  API-->>Browser: observationId + accepted state
  QA->>QA: Continue other test cases
  API->>Worker: Enqueue analysis
  Worker->>Context: Fetch scoped AC and candidate code
  Context-->>Worker: Source references + excerpts
  Worker->>AI: Minimal relevant facts + evidence references
  AI-->>Worker: Structured diagnosis and Jira draft
  Worker->>Store: Validate and persist result
  Worker-->>Review: Ready for human review
  QA->>Review: Inspect evidence, correct and approve
  Review->>API: Approve draft / publish intent
  API->>Jira: Create issue + allowed attachments
  Jira-->>API: Issue key
  API-->>Review: Jira link / publication status
~~~

## Core objects (draft schemas)

- **Observation:** QA-entered scenario, steps, expected and actual, env, capture IDs.
- **EvidenceBundle:** itemized steps/screenshots/console/network with timestamp, source, sensitivity and capture gaps. Does not mean all raw payloads may be sent to models.
- **DiagnosisReport:** fact references, evidence-backed inferences, hypotheses, unknowns, suggested fault domain and missing evidence.
- **JiraDraft:** readable expected/actual/repro, attached item references, diagnosis note, route recommendation and approval state.

See [JSON Schema drafts](../../schemas/) and [example](../../examples/fictional-bug.md).

## Minimal server endpoints — illustrative, not frozen

| Operation | Purpose |
| --- | --- |
| POST /observations | Ingest validated metadata and start a job |
| POST /observations/:id/artifacts | Upload bounded evidence with access control |
| GET /observations/:id | Capture / analysis status |
| GET /observations/:id/draft | Human-readable draft and evidence links |
| PATCH /observations/:id/draft | QA corrections |
| POST /observations/:id/approve | Approval and idempotent Jira publication |

Splitting metadata and large artifacts is an implementation option, **not** a requirement for v0.1. Endpoint shapes are placeholders only.

## Evidence pipeline is not an indiscriminate HAR upload

1. Capture short replay steps and only bounded network/console activity needed around the failure.
2. Associate actions, request IDs, timestamps and screenshots with a common capture.
3. Redact cookies, authorization headers, credentials, PII, tokens, and sensitive payload fields **before upload whenever possible**, then again at server ingress.
4. Store raw approved evidence separately from model-ready summaries; minimize exposure and set retention/deletion controls.
5. Pass only relevant evidence and excerpted code/criteria to AI with stable reference IDs.
6. Validate model output format and ensure every strong conclusion cites specific evidence.
7. Route uncertain diagnosis as suggestion; do not silently auto-assign a developer.

## Chrome integration options (to test)

- Recorder interoperability for user action paths; it does not capture all required console/network context by itself.
- chrome.debugger / CDP for event and network/runtime evidence, subject to debugger permissions and interference with DevTools sessions.
- DevTools extension APIs for targeted export or evidence collection, potentially requiring DevTools to be open.
- Existing browser automation/capture tools as fallback; **do not** invent a new general-purpose browser debugger.

Source maps should help resolve stack traces into readable original source. Disabling JS minification by default is not required. Static source branch matching is only **candidate** provenance and must not be represented as a verified deployed artifact.

## AI runtime is a material open decision

Current human coding subscriptions are **not assumed** to be embeddable inference endpoints. Validate an authorized model API, enterprise offering or approved runner, with security terms, retention, concurrency, observability and cost before building the worker.

## No trustworthy evidence → no overclaim

| Evidence | Safe output |
| --- | --- |
| Description only | Stable bug draft + symptom class |
| Browser action + errors | Targeted frontend investigation suggestion |
| Correlated API response | Evidence-backed boundary / API hypothesis |
| Cross-service trace and allowed logs | Deeper service-chain hypothesis |
| Source and verified deployed build | Implementation-level diagnosis, still not automatic proof |

Source code on its own does not prove which branch was deployed. Backend diagnosis requires service owners to validate available telemetry and cross-service correlation.

## Recovery

Capture failure must not lose QA notes. Analysis timeout must lead to an actionable minimal draft, not indefinite blocking. Jira creation must be idempotent and errors visible to the reviewer.
