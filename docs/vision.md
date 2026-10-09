# Vision, problem, and boundaries

Status: **Baseline principles accepted in discussion; implementation not yet approved.** Date: 2026-10-09.

## Why

Engineering teams may already use coding agents, yet defects still travel through weakly structured human communication. A QA observation becomes a screenshot, a short Jira description, a chat message, a call to an off-site developer, a reassignment, and finally a prompt for a coding agent. That loses context and repeats expensive discovery work.

The goal is **high-quality, fast, engineering-ready Jira**, and over time to connect the business intent, tested behavior and runtime evidence throughout the engineering lifecycle.

## Intended outcome

A QA engineer describes a discrepancy using ordinary business language and captures a reproducible browser session. The system takes responsibility for gathering and organizing facts, resolving relevant requirement context, suggesting a **bounded** diagnosis, and preparing a structured issue. The QA engineer verifies what was observed and expected before publication. Developers and their agents should be able to start investigation without first reconstructing the entire observation through meetings.

The same principles may extend earlier: PM/QA prepare acceptance criteria and tests against business rules, while developers and agents compare the planned behavior with existing code and services.

## Three distinct information authorities

| Information | Governs | Typical authority |
| --- | --- | --- |
| Business intent / acceptance criteria | Expected behavior | Approved product decisions / Confluence |
| Implementation | How behavior is implemented | Application source and configuration |
| Runtime evidence | What happened in a particular run | Browser, APIs, logs and tracing |

One source cannot silently replace another. If they disagree, preserve the disagreement for review rather than manufacture a single confident answer.

## Human/tool/AI contract

| Role | Responsibility | Not required |
| --- | --- | --- |
| PM | Define and decide business behavior, exceptions and trade-offs | Inspect each code path manually |
| QA | Identify test context, observe discrepancies, review facts and expectation | Know service ownership or hand-write diagnosis |
| Developer / owner | Diagnose and change implementation, review uncertain routing | Re-interview QA for ordinary captured facts |
| Deterministic tools | Capture, redact, store, link, validate, call APIs | Infer undocumented business intent |
| AI | Summarize, compare, classify and explain with provenance; ask for missing evidence | Pretend hypotheses are verified facts |

## First track and exclusions

**Track B — QA observation → evidence → reviewable Jira** is the first implementation track. Track A — PRD/business knowledge/pre-test preparation — is important input context, not an excuse to rebuild SDLC first.

Not first-release requirements: automatic root-cause proof; automatic code repair; generic test data platform; full-scale Confluence mirror; exact per-feature deployment provenance; auto-assignment to individuals; replacing existing coding-agent subscriptions with unsupported API assumptions.

## Success metrics (targets to baseline, not invented numbers)

- Time from QA observation to developer-actionable issue.
- Fraction of Jira bugs accepted without basic clarification requests.
- Reproducibility / evidence completeness for relevant issue types.
- QA hands-on effort per issue.
- Incorrect team routing and reopen/reassignment rate.
- Evidence capture failure rate, sensitive data incidents, diagnosis corrections.

Measure against the current manual process before claiming improvement.

## Public disclosure boundary

This repository documents abstract design. Company-specific PRDs, system maps, internal URLs, HAR captures, telemetry, identities and credentials must remain in controlled storage; this repo may store only sanitized interfaces and examples.
