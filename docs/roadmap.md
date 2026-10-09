# Roadmap, feasibility and exit gates

Status: **Proposed sequencing**; no implementation commitment or schedule estimate.

## Phases and gates

| Stage | Deliverable | Exit gate | Not required yet |
| --- | --- | --- | --- |
| Phase 0 — technical spike | One synthetic Chrome reproduction → draft → reviewed Jira creation | Can capture useful evidence; legal/secure inference available; Jira API permissions verified | Full product UX |
| v0.1 — QA to Jira | Short capture + observation + structured evidence + asynchronous draft + QA confirmation + Jira | QA does not manually retype bug; minimal issue correct; errors visible; redaction passes | Exact root-cause proof, team auto-assignment |
| v0.2 — context-rich frontend diagnosis | Targeted AC + frontend source and source maps; evidence-backed fault-domain hints | Traceable diagnosis, measurable reduction in clarification | General knowledge mirror |
| v0.3 — backend and routing | Service logs/traces, system ownership, validated team routing | Cross-service request correlation; routing policy reviewed | Autonomous code changes |
| Later — requirement and test preparation | PRD preflight, scenario generation, safe data provisioning and regression linkage | Distinct user and security acceptance gates | Universal automated SDLC |

## Feasibility matrix (initial hypotheses)

| Module | Value | Difficulty | Dependency | Evidence reliability | Priority |
| --- | --- | --- | --- | --- | --- |
| Standard Jira draft/API | High | Low–medium | Jira permission + schema | High after deterministic validation | Immediate |
| Browser action/console/network capture | High | Medium | Chrome permissions / CDP compatibility | To validate per signal | Immediate spike |
| QA review UI | High | Low–medium | Auth + draft persistence | High for QA-verified facts | v0.1 |
| Contextual AC lookup | High | Medium | Confluence authority/permissions | Depends on document currency | Minimal early, deepen v0.2 |
| Source map / repository investigation | Medium–high | Medium | Maps, branch candidates, code access | Probabilistic without deployed SHA | v0.2 |
| Backend request/trace analysis | Potentially high | High / unknown | Service tracing, log owners, access | Unknown until observability reviewed | v0.3 |
| Auto route to team | Medium–high | Medium | Maintained ownership contract | Unknown until historical evaluation | Suggest first |
| Automatic test data | Potentially high | High | Safe setup/reset APIs | Scenario-specific | Later |
| Full PRD preflight | High potential | Medium–high | Rule quality / code linking | Human review required | Parallel pilot |

## Validation measures

Baseline current median / p90 time to developer-actionable issue, clarification loops per issue, issue reproducibility, misrouting and QA work per issue. Compare the same categories after rollout. Do not assert percentages before an observed pilot.

## Decision gates after spike

**Proceed to v0.1** only after confirming: (1) Chrome capture offers useful reproducible evidence; (2) a secure AI runtime is callable by service; (3) intake/redaction and storage approach is acceptable; (4) QA can review and publish a minimum Jira via authenticated API.

If CDP recording is impractical, fall back to narrower browser collection or guided evidence import while preserving the same domain contracts. If model access is blocked, first deliver deterministic Jira templating and evidence attachments, then add AI asynchronously.

## Explicitly excluded until evidence changes

Universal log search, automatic individual assignment, agent fixing production bugs, full service orchestration, all-system documentation mirroring, generic test-account provisioning, all-day session recording, and feature-branch-to-deployment provenance platform.

For practical experiments see [QA capture spike](validation/qa-capture-spike.md).
