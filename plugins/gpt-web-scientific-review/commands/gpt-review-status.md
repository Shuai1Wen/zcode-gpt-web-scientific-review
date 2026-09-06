---
description: Inspect the current GPT Web scientific-review job state without disturbing ChatGPT or changing the review.
argument-hint: "[job-id]"
skills: gpt-web-orchestrator, gpt-pro-watch
disable-noninteractive: false
---

Report the state of the requested job, or the newest active job when no id is supplied:

$ARGUMENTS

Read `.gpt-web-review/jobs/*/state.json` and existing artifacts. Do not submit any browser message and do not change model selection.

Return compactly:

- job id;
- requested mode and literal visible model label;
- state;
- submitted time;
- last heartbeat and heartbeat count;
- Temporary Chat yes/no/unknown;
- which artifacts exist;
- blocking condition, if any;
- next safe action.

If a Pro job is active and this invocation is itself being used as a heartbeat, follow `gpt-pro-watch` exactly.
