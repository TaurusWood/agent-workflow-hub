# Bug lifecycle: observation to actionable Jira

Status: **Target workflow** (review is intentional; automation details are proposed).

~~~mermaid
flowchart TB
  CASE["QA executes test case"] --> ISSUE{"Unexpected behavior?"}
  ISSUE -->|No| NEXT["Continue testing"]
  ISSUE -->|Yes| START["Start short capture / reproduce"]
  START --> NOTE["QA submits scenario + observed / expected"]
  NOTE --> ACCEPT["Service intake / persist evidence"]
  ACCEPT --> NEXT
  ACCEPT --> ENRICH["Background: redact, analyze & correlate"]
  ENRICH --> REPORT["Diagnosis report + structured Jira draft"]
  REPORT --> READY{"QA review"}
  READY -->|Approve / edit| CREATE["Service creates Jira with evidence references"]
  READY -->|Not ready| MORE["Revise expectation or recapture evidence"]
  MORE --> ENRICH
  CREATE --> ROUTE["Notify / route team (policy-driven)"]
  ROUTE --> FIX["Developer / agent investigates & fixes"]
  FIX --> VERIFY["QA verifies against scenario"]
  VERIFY -->|Resolved| CLOSE["Close according to team process"]
  VERIFY -->|Still failing| ISSUE
~~~

## Handoffs

| Step | Human | Deterministic system | AI | Exit / checkpoint |
| --- | --- | --- | --- | --- |
| Discover | QA detects and identifies scenario | Can surface linked test case | — | Observation |
| Capture | QA initiates and reproduces | Captures actions, screenshot, runtime signals | — | Evidence bundle or capture gap |
| Submit | QA gives brief natural-language actual/expected | Persists and confirms intake | — | QA **may continue testing** |
| Enrich | — | Redacts, fetches only relevant context, tracks job state | Assesses evidence and identifies hypotheses | Diagnosis and draft |
| Review | QA checks facts, expected behavior, privacy and emphasis | Displays links, supports edits, blocks invalid submission | May propose clarification | Approval / revision |
| Publish | QA authorizes | Jira API call; attachments; deduplication key; notifications | No autonomous privileged action | Created Jira or explicit failure |
| Resolve | Developer / owner | Source, telemetry, issue lifecycle | Coding agent may use structured Jira | Fix + verification evidence |

**Do not confuse** service acceptance of evidence with creation of Jira. If background enrichment fails, users must see the failure and can fall back to a minimal compliant draft. No silent loss.

## Required Jira minimum

1. Environment, scenario and test context.
2. Reproduction steps (manual or captured, with uncertain steps labeled).
3. Expected behavior and its source when known.
4. Actual behavior.
5. Symptom classification; attachments and evidence links when available.
6. Evidence limitations and diagnosis confidence explicitly expressed.
7. Suggested team, **not assumed assignee**, unless approved routing policy exists.

The minimum remains useful without source access or trace data. Avoid blocking issue creation on an unproven root cause.

## One fictional example

**Scenario:** A guest proceeds from booking summary to payment.

**Observed:** Loading indicator persists after clicking Continue.

**Expected:** Payment step opens when the remaining balance is nonzero, according to an explicitly linked accepted criterion; if no accepted criterion is retrievable, mark expected behavior as QA-provided and needing confirmation.

**Evidence:** Captured button click, redacted request metadata, one screenshot. The API fault domain is a hypothesis until the network / trace evidence supports it.

**Draft:** Clear steps, actual/expected, environment, evidence links and routing recommendation. QA approves before Jira creation.

## Safety/operability boundaries

Short captures are preferred over always-on recording. Redact tokens, PII, cookies and sensitive request bodies before model processing or issue attachment. Automatic team notification comes **after** a valid Jira is created. Failures are retriable; duplicate submissions should not create duplicate issues.
