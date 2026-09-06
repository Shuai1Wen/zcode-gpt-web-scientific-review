---
description: Safely resume a paused or interrupted GPT Web scientific-review workflow from its persisted job state without duplicating the external review.
argument-hint: "[job-id]"
skills: gpt-web-orchestrator, gpt-web-browser, gpt-pro-watch, gpt-review-adjudicator
disable-noninteractive: true
---

Resume the requested GPT Web review job, or the newest incomplete job if no id is supplied:

$ARGUMENTS

First read `state.json` and existing artifacts. Continue from the earliest incomplete phase. Never automatically resend the original prompt merely because the ZCode session was interrupted.

Recovery rules:

- `RUNNING_PRO`: locate and inspect the existing tab; use heartbeat behavior only.
- `COMPLETED`: extract and freeze if not already frozen.
- `EXTRACTED`: continue to challenge/adjudication; do not rerun blind review.
- `CHALLENGE_COMPLETED`: adjudicate.
- `AUTH_REQUIRED`: ask the user to complete authentication manually, then re-inspect.
- `MODEL_UNAVAILABLE`: do not downgrade unless the user explicitly changes policy.
- `BROWSER_LOST`: recover only from a normal stored conversation URL when possible; do not use secret browser state or hidden endpoints.
- `SUSPECTED_STALL`: preserve the job and request user approval before any destructive recovery action.

If `response_raw.md` is frozen, treat it as immutable evidence.
