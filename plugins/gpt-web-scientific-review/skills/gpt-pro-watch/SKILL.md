---
name: gpt-pro-watch
description: Monitor an already-submitted long ChatGPT Web Pro scientific-review job without disturbing it. Use for the scheduled ~30-minute heartbeat, Pro status checks, recovery classification, and completion detection. Heartbeats are read-only and must never prompt, retry, refresh without cause, downgrade, or interrupt the Pro run.
when_to_use: Use only after a Pro review prompt has been submitted and until the response is extracted or a real blocking state is observed.
license: MIT
metadata:
  version: 0.1.0
---

# Pro Heartbeat Protocol

## Why this skill exists

A long Pro review should be allowed to run. Monitoring must not become interference.

ZCode scheduled automations currently support Hour as the smallest repeat unit. Approximate a 30-minute heartbeat with two hourly tasks:

```text
Heartbeat A: every hour at minute 00
Heartbeat B: every hour at minute 30
```

Bind both to the same coordinator/review session when possible.

## Setup invariant

The project should have `.gpt-web-review/coordinator.json` containing only non-secret coordination metadata, for example:

```json
{
  "heartbeat_protocol": "dual-hourly",
  "heartbeat_a_minute": 0,
  "heartbeat_b_minute": 30,
  "keep_awake_required": true
}
```

The automation definition itself lives in ZCode, not in this plugin repository.

## Heartbeat input

A heartbeat should identify the active Pro job from `.gpt-web-review/jobs/*/state.json` where `status` is one of:

```text
SUBMITTED
RUNNING_PRO
SUSPECTED_STALL
```

If there is no active Pro job, do nothing except report `NO_ACTIVE_PRO_JOB`. Never create a ChatGPT request merely because a heartbeat fired.

## Read-only heartbeat procedure

1. Read the active job state.
2. Locate the existing ChatGPT browser tab/conversation associated with the job.
3. Observe only. Do not send a message.
4. Record visible signals:
   - tab exists;
   - URL/conversation identity matches when available;
   - generation/thinking/working indicator present or absent;
   - Stop control present or absent;
   - assistant response present;
   - composer available;
   - explicit error/rate-limit/auth message present;
5. Compare to the previous heartbeat summary.
6. Increment `heartbeat_count` and update `last_heartbeat_at`.

## Allowed outcomes

### Still running

If active generation is visible or completion is ambiguous:

```text
status = RUNNING_PRO
heartbeat_result = STILL_RUNNING
```

Action: none.

### Completed

Declare completion only when the browser protocol's completion criteria are satisfied. Then:

```text
status = COMPLETED
heartbeat_result = COMPLETED
```

The orchestrator should extract/freeze the response next.

### Authentication required

Only with explicit login/security UI:

```text
status = AUTH_REQUIRED
```

Do not attempt credential automation.

### Rate limited

Only with explicit rate/usage-limit UI:

```text
status = RATE_LIMITED
```

Do not rotate accounts or retry through another account.

### Browser lost

If the required tab is missing:

- if a normal conversation URL was stored and can safely be reopened, attempt one normal navigation and inspect;
- if the job used Temporary Chat and cannot be recovered, set `BROWSER_LOST`;
- never use browser-profile extraction or hidden tokens to recover it.

### Suspected stall

If multiple consecutive heartbeats show no visible progress and no explicit error, increment `unchanged_heartbeats`.

Recommended classification threshold:

```text
unchanged_heartbeats >= 4 -> SUSPECTED_STALL
```

This is a warning, not permission to interrupt. Preserve the job and ask the user before any destructive recovery action.

## Forbidden heartbeat actions

Never:

- click Stop;
- click Retry/Regenerate;
- send follow-up text;
- send "continue";
- resend the original prompt;
- reload only because time has passed;
- switch model;
- duplicate the conversation;
- create a new job;
- modify the scientific prompt;
- mark `FAILED` merely because the run is long.

## Keep-awake requirement

ZCode automations run locally. For long Pro jobs, the user should enable ZCode's global **Keep awake** switch and keep ZCode running. If the computer/app is unavailable, record that the heartbeat was missed rather than pretending the browser was checked.

## Heartbeat output

Keep it short:

```text
GPT Web Pro heartbeat
job: <id>
status: RUNNING_PRO | COMPLETED | ...
heartbeat: <n>
visible change: <brief factual observation>
action: none | extraction requested | user action required
```
