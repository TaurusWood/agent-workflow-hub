# Synthetic walkthrough: guest checkout loading

**All data are fictional** — no live customers, applications, services or screenshots.

QA observes persistent loading after clicking Continue on a guest booking summary. A short recording yields a click and a payment preparation request returning HTTP 500. The mock screenshot is a reference placeholder, not a real attachment.

The output separates: **fact** (HTTP 500 in captured request); **inference** (API boundary implicated); **hypothesis** (UI might fail to leave loading on request error); **unknown** (actual server root cause). The acceptance criterion is not linked, so the expected behavior is explicitly QA-reported rather than verified.

The Jira draft stays pending QA review. QA may correct the expectation or request more evidence before creation.

Records: [Observation](observation.json) · [EvidenceBundle](evidence-bundle.json) · [DiagnosisReport](diagnosis-report.json) · [JiraDraft](jira-draft.json).

A downstream system must not treat a passing JSON Schema check as evidence that payloads are safe, correct or approved.
