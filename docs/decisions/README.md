# Decisions and open questions

This register separates **accepted direction**, **proposal**, and **unverified assumption**. The mere presence of text here does not constitute a frozen technical contract or team approval.

## Accepted direction from discussion (2026-10-09)

| ID | Direction |
| --- | --- |
| D-01 | Improve Jira quality and QA→developer handoff; do not require QA to author engineering diagnosis. |
| D-02 | QA discovers and describes the discrepancy; deterministic tools gather facts; AI classifies and drafts; people review key behavior claims. |
| D-03 | Business rules/AC are important assets separate from code and runtime evidence. |
| D-04 | Evidence-backed diagnosis must distinguish fact, inference, hypothesis and unknown. |
| D-05 | QA should be able to continue testing after observation submission; analysis need not block the session. |
| D-06 | Browser capture and frontend transparency are high-value initial directions; short capture on observed issue is preferred to passive continuous recording. |
| D-07 | Jira creation should follow QA review/confirmation at this maturity level. |
| D-08 | Test-data automation and broad PRD/SDLC changes are future/parallel tracks, not blockers for the QA-to-Jira MVP. |
| D-09 | Current repo is **public**; never store real internal evidence, maps, source, credentials or business documents. |

## Proposals awaiting engineering validation

| ID | Proposal | Required verification |
| --- | --- | --- |
| P-01 | Chrome extension + CDP/Recorder-based evidence collection | Permissions, DevTools conflict, fidelity, UX |
| P-02 | Small QA Assistant API, background analysis, review surface | Security, operational ownership, persistence |
| P-03 | Candidate QA/Staging branch as code lookup default | Branch drift and deployed-code mismatch |
| P-04 | Model inference via authorized service-side provider/adapter | Entitlement, cost, privacy and concurrency |
| P-05 | Typed Observation, EvidenceBundle, DiagnosisReport and JiraDraft | QA/engineering review and realistic samples |
| P-06 | Phased rollout Phase 0 → v0.1 → v0.2 → v0.3 | Pilot measurements and resourcing |

## Questions requiring team participation

1. QA: What is the typical bug path today? What capture interaction can be performed in seconds?
2. Frontend: Source maps in QA/Staging? Stable selectors? Can CDP/network evidence be collected under browser policies?
3. Backend: How do requests correlate across 3–4 services? Are trace IDs, logs and test data APIs available?
4. PM: Which approved documents can serve as reliable expected behavior? Who settles contradictions?
5. Jira/project admin: Required fields, attachment limits, write rights, deduplication and notifications?
6. Security/platform: What evidence may be captured, retained, sent to model, attached to Jira?
7. Platform/AI: Which inference provider is legally and technically callable by backend service?

## Change process

Each material decision should record: decision, alternatives considered only where material, supporting evidence, owner, date and scope. Upgrade P to accepted only after explicit review/approval, not because no one objected. Avoid overbuilding an ADR bureaucracy before the first technical spike.
