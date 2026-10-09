# Model runtime access — local plan vs. shared API

**Status: verified external capabilities; proposed implementation options, not an accepted architecture.** Date: 2026-10-09.

## Key correction

ChatGPT and OpenAI Platform API have separately billed standard access. **However**, OpenAI now supports Sign in with ChatGPT (SIWC) for eligible open-source / local apps: with explicit user OAuth consent, a tool can make eligible Responses API requests using the user's ChatGPT plan allowance. This is a restricted grant, not a generic OpenAI API key and not access to user chat history. A public documentation repository is not in itself proof that a remotely hosted enterprise application is eligible.

## Options

| Runtime | Phase 0 use | Shared service fit | Material constraint |
| --- | --- | --- | --- |
| ChatGPT-authenticated Codex CLI (noninteractive exec / app-server) | Fast local synthetic proof | Not automatically a central multi-user service | Identity, quotas, runner security, operations |
| SIWC OAuth plan-backed Responses API | Local open-source companion app experiment | Remotely hosted/paid access requires relevant enrollment | Each user's consent, supported features and plan limits |
| Independently billed Platform API | Good for synthetic proof and central service | Preferred default for a shared team backend | Budget, service credentials, security approval |
| No AI | Standard Jira template + safe evidence | Always valid fallback | No AI diagnosis |

## Local trial

Browser capture → trusted local evidence/redaction worker → Codex CLI or OAuth-authorized model runtime → structured diagnosis draft → QA review → Jira API.

## Shared service target

Browser capture → authenticated intake + encrypted evidence store → background processing + scoped context retrieval → approved API model runtime → validated structured report → QA review → Jira API.

Use one internal ModelRuntime adapter boundary, not a speculative multi-provider platform. Model processing only sees necessary sanitized evidence + scoped context. The service, not the model, owns authentication, retention, publication permission and idempotency.

## Conditions verified (2026-10-09)

- Codex CLI supports scripted noninteractive execution (codex exec).
- SIWC requires a user-authorized scope for plan usage. SIWC Responses calls must set store:false and stream:true; background requests and several hosted tools are unavailable through this route.
- SIWC user requests share the person's subscription limits; they do not create a separate quota.
- The supported launch target is eligible open-source/local tooling. OpenAI's docs require interested paid/remote app builders to request access. Do not assume a shared company-hosted QA backend is approved.
- ChatGPT Business/Enterprise may have separate Codex noninteractive access-token capabilities, subject to workspace/admin policy; do not share an individual's credentials as a team service identity.
- Regardless of runtime, QA approval remains the gate for publishing Jira.

## Recommendation

**Spike:** Test local Codex exec with a synthetic EvidenceBundle for fast validation. Optionally test the SIWC route if a local, user-authorized open-source client is worth distributing.

**Production candidate:** Prefer company-governed separately billed API runtime for asynchronous jobs across many QA users, unless approval for another official entitlement route is obtained. Keep model provider isolated behind a small adapter; changing model billing should not require a redesign of the capture, review or Jira flow.

## Source links

- [SIWC overview and eligibility](https://developers.openai.com/siwc/token-sharing-open-source)
- [Open-source SIWC example](https://developers.openai.com/cookbook/articles/sign-in-with-chatgpt)
- [SIWC preview limitations](https://developers.openai.com/siwc/token-sharing-open-source/preview-limitations)
- [Codex CLI documentation](https://learn.chatgpt.com/docs/cli/reference)
- [ChatGPT and API separate billing](https://help.openai.com/en/articles/9039756-managing-billing-settings-on-chatgpt-web-and-platform)
- [Plan usage in external applications](https://help.openai.com/en/articles/20001542-using-your-chatgpt-plan-in-other-apps-and-sites)
