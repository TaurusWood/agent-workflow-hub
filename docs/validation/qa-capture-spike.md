# Technical Spike: Chrome capture → AI draft → human-reviewed Jira

Status: **Next proposed experiment**. Use a fictional demo app, approved non-sensitive test environment and test account only.

## Objective

Demonstrate whether a QA user can reproduce a simple failure, submit a short observation, and receive a useful **reviewable** Jira draft linking the steps, evidence and bounded diagnosis. Then verify that QA approval creates an issue through Jira API with correct attachments and provenance.

**Not** a commitment to a particular extension architecture or AI provider.

## Experiment in six slices

1. **Capture:** Record user actions, a screenshot, console error, and selected Network requests through Chrome-native interfaces. Compare Recorder export, CDP debugger and DevTools entry points. Report missing signals.
2. **Transparency:** Test stack trace → source map → readable source location on a synthetic frontend failure. Record failures when sources are stale/unavailable.
3. **Bundle:** Build a bounded evidence bundle with action/request correlation, redaction, capture gaps and stable evidence IDs.
4. **Inference:** Send only sanitized relevant snippets to an authorized model API/runtime; return explicit fact/inference/hypothesis/unknown and structured draft. Validate model result on server.
5. **Review:** QA can inspect the observation, evidence, inferred domain and draft; edit expectations; approve or reject. QA need not wait while processing.
6. **Jira:** With approved test project rights, post idempotently, upload/link safe attachments, notify intended team, and display the issue key and errors.

## Acceptance checklist

- [ ] QA can start/stop capture and record at least a click/repro step without specialist DevTools expertise.
- [ ] Network and console evidence can be correlated to the capture, with gaps displayed rather than hidden.
- [ ] Token/PII-like fixture strings do not leak to model request or Jira attachment.
- [ ] No false claim that a candidate source branch is the deployed build.
- [ ] Human-review UI distinguishes QA observation, retrieved facts and AI hypotheses.
- [ ] API handling includes failed analysis, retry, cancelled job and duplicate Jira publish intent.
- [ ] Jira contains environment, steps, expected, actual, evidence references and uncertainty even when diagnosis fails.
- [ ] Baseline manual Jira preparation time is measured on comparable tasks.

## Cost and risk questions to measure

- Chrome debugger permissions, coexistence with open DevTools, extension deployment policies.
- Captured artifact size, memory use, latency and browser versions.
- Redaction effectiveness; storage/retention and allowed model data handling.
- LLM calls/token usage and whether model plans offer a **programmatic API** (do not assume).
- QA review time and proportion of mischaracterized evidence.
- Jira editor/attachment API behavior and permissions in the actual team project.

## Scope control

If one slice fails, log the blocker and use a smaller fallback (e.g., selected screenshot + console + manually imported sanitized HAR) rather than building a full capture platform. Invite QA, FE, backend, PM, platform/security and Jira admin to the outcome review.

The team should **not** start a generic test-data platform or multi-service log architecture before resolving this experiment.
