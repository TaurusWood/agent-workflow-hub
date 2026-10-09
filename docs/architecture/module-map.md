# Logical modules and owner contributions

Status: **Candidate modular decomposition**, not a microservice plan.

| Capability | Product responsibility | Likely contributors | v0.1 disposition |
| --- | --- | --- | --- |
| Observation & Capture | QA entry, reproducible steps, browser evidence | QA + Frontend | Essential; PoC first |
| Evidence intake & governance | Validation, redaction, storage, retention, correlation | Platform / Backend + Security | Essential |
| Context resolution | Targeted PRD/AC lookup, env → candidate repo mapping | PM / Tech leads + Platform | Minimal lookup only |
| AI diagnosis and structuring | Grounded classification, uncertainty, report, Jira text | AI/platform + Frontend | Bounded; never gate on root cause |
| QA review & publication | Readable linked evidence, edit, approval, Jira API | QA + Platform | Essential |
| Ownership and notification | Suggest team, validated routing rules, notify | Engineering leads + Jira admin | Suggest only initially |
| Backend telemetry | Request / trace / service error read | Backend + SRE | Follow-up, gated by availability |
| Test data provisioning | Precondition lookup/creation/reset | QA + Backend | Later; not a platform prerequisite |
| PRD preflight | Existing rules & code impact hints | PM + Engineering | Parallel candidate experiment |

## Implementation grouping

For a small first release, **one browser integration + one QA Assistant application** is a viable hypothesis. That application may contain ingestion, background analysis, review and Jira adapters. Logical capabilities do not imply separate deployments.

Do not turn every row into an independent repo, skill or agent.

## Tool vs agent boundary

- Tools/connectors: precise reads and writes (code search, fetch approved AC, attach file, create Jira) with typed permissions and observable failure.
- Deterministic application: validation, redaction, auth, retention, rate limits, task state, idempotency, approval enforcement.
- AI/agent: select scoped evidence, explain comparisons, draft expected/actual, bounded fault-domain inference, cite evidence and mark unknowns.
- Human: decide intended behavior, correct false assumptions, approve external publication and engineering work allocation policy.

## Baseline API and ownership assumptions that must be tested

- Jira project permissions and allowed required fields.
- GitHub/GitLab read permission to approved repositories; no local checkout for QA.
- Confluence document permission; do not mirror all documents without an owner.
- Capture permission within enterprise Chrome policy.
- Safe ownership mapping from real systems; public repo holds **examples only**.
- Approved service-to-model access, including data handling terms.
