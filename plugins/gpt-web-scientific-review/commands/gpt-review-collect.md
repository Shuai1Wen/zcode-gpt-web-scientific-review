---
description: Collect and synthesize the artifacts from a completed or partially completed GPT Web scientific-review job without rerunning ChatGPT.
argument-hint: "[job-id]"
skills: gpt-web-orchestrator, gpt-review-adjudicator
disable-noninteractive: false
---

Collect the requested job, or the newest job if no id is supplied:

$ARGUMENTS

Do not open a new ChatGPT request. Read the persisted artifacts and produce a concise package summary:

1. central scientific question;
2. requested/visible model class;
3. blind-review verdict;
4. challenge-phase changes, if any;
5. final conflict matrix/adjudication;
6. required core method changes;
7. required core experiments;
8. supporting/robustness/engineering notes;
9. unresolved questions;
10. file paths for every available job artifact.

If adjudication is missing but the frozen external review exists, complete adjudication from existing evidence rather than rerunning the external reviewer.
