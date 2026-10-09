# Draft schemas — not frozen contracts

These four JSON Schema Draft 2020-12 documents separate QA input, runtime facts, model reasoning and the human-reviewed Jira draft.

| Schema | Role |
| --- | --- |
| observation.schema.json | QA report and provenance of expected behavior |
| evidence-bundle.schema.json | Redacted evidence, references and missing capture signals |
| diagnosis-report.schema.json | Grounded claims explicitly labeled fact / inference / hypothesis / unknown |
| jira-draft.schema.json | User-editable issue with an approval state |

**Discussion artifacts only.** Missing intentionally: full authorization, upload protocol, retention lifecycle, schema negotiation, tenant-specific Jira fields, idempotency keys, audit details and executable service boundaries. Do not treat them as production API contracts.

## Invariants to preserve

- Evidence facts are not overwritten by new model opinions.
- Claims have stable references to evidence where available; absent support must be labeled unknown/hypothesis.
- Expected behavior distinguishes QA expectation from approved acceptance criteria.
- Capture gaps are explicit.
- Uploaded payloads and artifact links must be access controlled, redacted and retained under a documented policy.
- Only an authenticated human approval may trigger Jira publication in the first release.

Use [fictional examples](../examples/fictional-bug.md) in design reviews; validate contracts against a sanitized technical spike before freezing.
