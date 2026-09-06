---
description: Force a focused independent scientific review through ChatGPT Web using the Extra High reasoning class only.
argument-hint: "<review target>"
skills: gpt-web-orchestrator, gpt-scientific-review, gpt-web-browser, gpt-review-adjudicator
disable-noninteractive: true
---

Run the complete blind scientific-review workflow for:

$ARGUMENTS

Force:

```text
requested_mode = EXTRA_HIGH
allow_fallback = false
```

Do not use Pro unless the user starts a new request that explicitly changes the mode. Do not silently use a lower reasoning class.

Build the blind packet, verify Extra High in ChatGPT Web, submit once, wait for genuine completion, freeze `response_raw.md`, and perform evidence-based adjudication. Run the challenge phase when there is a substantive conflict with ZCode's current proposal.
