---
description: Force a publication-level or project-critical independent scientific review through ChatGPT Web using Pro only, with long-run heartbeat monitoring.
argument-hint: "<review target>"
skills: gpt-web-orchestrator, gpt-scientific-review, gpt-web-browser, gpt-pro-watch, gpt-review-adjudicator
disable-noninteractive: true
---

Run the complete blind scientific-review workflow for:

$ARGUMENTS

Force:

```text
requested_mode = PRO
allow_fallback = false
```

Before submission, verify the visible Pro selection in ChatGPT Web. If Pro cannot be selected or verified, set `MODEL_UNAVAILABLE` and do not submit to another model class.

After submission:

- set `RUNNING_PRO`;
- preserve the browser tab;
- use the configured dual-hourly heartbeat protocol (:00 and :30) for approximately 30-minute read-only checks;
- do not send follow-ups, click Stop/Retry, refresh due only to elapsed time, or duplicate the request;
- when completion is verified, freeze the raw response first;
- then run adversarial comparison if useful and perform evidence-based adjudication.

If heartbeat automations have not been configured, provide the exact `/gpt-review-setup` action needed. Do not fake scheduled monitoring.
