# Agent Workflow Hub

> AI-assisted engineering collaboration: from business intent to verifiable execution evidence and actionable work items.

**Status:** Design baseline · 2026-10-09 · No production implementation.

This public repository records shared **principles, target workflows, proposed architecture and validation plans** for improving engineering collaboration. **Track B — QA observation → evidence → diagnosis → human review → Jira** is the first implementation track. Earlier SDLC activities (PRD, business rules, test preparation) are context and future integration points, not scope for a full platform build now.

## Read first

| Audience | Start here |
| --- | --- |
| Everyone | [Vision and boundaries](docs/vision.md) |
| PM / QA / Engineering | [End-to-end collaboration workflow](docs/workflows/requirement-to-verification.md) |
| QA / Frontend / Backend | [Bug lifecycle](docs/workflows/bug-lifecycle.md) |
| Architects / implementers | [System architecture](docs/architecture/system-overview.md) |
| Implementers | [Evidence and AI pipeline](docs/architecture/evidence-diagnosis-pipeline.md) |
| Leads | [Phased roadmap and gates](docs/roadmap.md) |
| Reviewers | [Confirmed, proposed and open decisions](docs/decisions/README.md) |

Mermaid diagrams are embedded in the Markdown files and render directly on GitHub.

## Operating principles

- **Business intent, implementation and runtime evidence are distinct sources:** none can silently replace another.
- **Human discovers and confirms; tools capture facts; AI explains and structures evidence.**
- **Evidence-first:** all diagnosis must separate observed facts, evidence-backed inference, hypothesis and unknown.
- **An actionable Jira is the outcome, not autonomous root-cause analysis.**
- **QA should not clone service repositories or manually transcribe technical diagnostics.**
- **Start with a reviewable Jira draft; automatic assignment and bug fixes require stronger evidence and controls.**
- **Build incrementally; do not assume a shared product rules mirror, universal test-data platform, or enterprise-scale agent infrastructure is needed for v0.1.**

## First target scenario

A QA engineer reproduces an issue in QA/Staging using a short browser capture. The tool collects operations, relevant console/network evidence and screenshots. An application service securely processes that bundle and calls a **configured model runtime** with only relevant business/code context. QA reviews the generated observation summary, expected/actual, evidence and proposed Jira, edits or approves, and the service creates Jira via its API. The user can continue testing while enrichment runs, and review is notified when ready.

**Important:** A consumer coding subscription does not automatically grant service-to-service inference API access. AI runtime/provider and entitlement are an explicit technical decision, not an assumed capability.

## Public repository policy

**Never commit:** internal Confluence exports, confidential PRDs, proprietary business rules, access tokens, tenant URLs, service endpoints, customer/user data, real HAR files, screenshots, stack traces, trace identifiers, private repo names or internal ownership maps. Examples in this repository are fictional. Keep sensitive mappings and evidence in appropriately access-controlled systems; any future sync design requires security review.

## What this repository is not

Not a deployed QA tool, not a source-of-truth mirror for internal company documents, not a replacement for Jira/Confluence/source repositories, and not an approved implementation contract. Documents mark each decision by status.

## Next step

Run the [Chrome capture → AI interpretation → QA review → Jira technical spike](docs/validation/qa-capture-spike.md) with synthetic or approved non-sensitive data. Use the results to set the v0.1 implementation boundary.
