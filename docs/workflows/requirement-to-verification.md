# Requirement → verification: shared engineering workflow

Status: **Target operating model**, not Phase 1 implementation scope.

~~~mermaid
flowchart TB
  IDEA["PM drafts change / PRD"] --> PREFLIGHT["AI-assisted preflight\nexisting rules + code capabilities"]
  PREFLIGHT --> DECIDE["Human product & engineering decisions"]
  DECIDE --> RULE["Approved business intent\nAC / scenarios / known exceptions"]
  RULE --> DEV["Developer + coding agent\ntechnical design & implementation"]
  RULE --> QA["QA + AI\nprepare test cases and data requirements"]
  DEV --> ENV["QA / Staging environment"]
  QA --> TEST["Execute agreed scenarios"]
  ENV --> TEST
  TEST -->|Unexpected| BUG["Capture → reviewable Jira"]
  BUG --> REPAIR["Developer / agent resolution"]
  REPAIR --> TEST
  TEST -->|Pass| VERIFY["Verification evidence and delivery"]
~~~

## Distinct responsibilities

**Product/PM:** Before the formal review, AI can identify existing rule conflicts, unhandled state transitions, missing acceptance criteria and potentially affected code. Human reviewers still decide ambiguous policy, trade-offs and new behavior. AI preflight reduces basic omissions; it does **not** make business sign-off automatic.

**QA:** Prepare coverage from approved criteria as early as possible, including happy paths, boundaries and permissions. Specify **test-data preconditions** independently of any tool that provisions them. During QA, capture observations; do not act as manual message router between services.

**Frontend:** Ensure QA/Staging is debuggable (prefer usable source maps), key controls have stable locators where useful, and request correlation can be recovered. Frontend is an initial investigation surface, not necessarily the origin of every UI symptom.

**Backend / SRE:** Decide how service errors, request IDs, trace propagation and allowed log queries can support fault-domain analysis across services. Backend introspection should not be invented by an external QA tool.

**Developers / agents:** Consume the same structured issue, linked evidence and behavior expectation; correct and verify rather than rediscover symptoms verbally.

## Business knowledge is not identical to code

- Business rules/approved criteria describe **ought**.
- Code/config describes **implementation**.
- Runtime evidence describes **what happened**.
- Requirements and implementation can diverge; the discrepancy must be exposed, not silently reconciled.

A future business knowledge layer may link Confluence document IDs, rule IDs, accepted changes, test cases, code references and ownership, without replacing the existing authoritative source.

## Test data is a separate concern

Start with explicit scenario requirements, e.g. Guest account; locale X; balance lower than order amount. Later validate an approved tool for finding or generating compliant test accounts and resetting state. Provisioning production-like personal data is prohibited without explicit controls.

## Implementation sequencing

Only the **Bug Capture / Diagnosis / Jira** slice is prioritized for the first PoC. PRD preflight, test-data orchestration and test-case generation are candidate parallel experiments, not dependencies that block v0.1.
