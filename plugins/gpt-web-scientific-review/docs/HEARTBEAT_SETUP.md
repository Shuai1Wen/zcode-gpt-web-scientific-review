# Pro Heartbeat Setup

## Why two tasks

ZCode scheduled tasks support Hour as the smallest custom repeat unit. To check a long Pro review approximately every 30 minutes, create two hourly tasks offset by 30 minutes.

## Coordinator session

Create the tasks **from the same ZCode session that owns the ChatGPT browser tab** whenever possible. The two tasks are shared across all Pro review jobs in that coordinator session; do not create a new pair for every job.

## Task A

**Title**

```text
GPT Pro heartbeat :00
```

**Schedule**

```text
Hourly, minute 00
```

**Instructions**

```text
Run the gpt-pro-watch heartbeat for the active `.gpt-web-review` Pro job in this session. Read the active state and inspect the existing ChatGPT Web tab only. If no active Pro job exists, report NO_ACTIVE_PRO_JOB. Never send a ChatGPT message, click Stop/Retry, refresh merely because time passed, switch models, resubmit a prompt, duplicate the conversation, or create a new review job. If completion is clearly verified, mark the job COMPLETED so extraction can proceed. If login, rate limit, browser loss, or another explicit blocking condition is visible, record the corresponding state and request user action where needed.
```

## Task B

**Title**

```text
GPT Pro heartbeat :30
```

**Schedule**

```text
Hourly, minute 30
```

Use the exact same instructions as Task A.

## Permissions

Use a read-only / lowest-change execution mode appropriate for inspection. The heartbeat itself does not need an expensive model or Pro reasoning; its job is to observe and update state conservatively.

## Keep awake

Enable **Keep awake** in ZCode Automations for long Pro jobs. ZCode and the computer must remain running/awake for scheduled tasks to execute.

## What a heartbeat may do

- read `state.json`;
- locate the existing ChatGPT tab;
- observe generation/composer/error state;
- increment heartbeat counters;
- classify still-running/completed/auth/rate-limit/browser-lost;
- request extraction after completion.

## What a heartbeat must never do

- send any message to ChatGPT;
- click Stop, Retry, Regenerate, Continue;
- refresh due only to elapsed time;
- switch Pro to Extra High;
- resubmit the blind prompt;
- create another chat to "check" the first;
- mark a long job failed merely for being long.

## Suspected stall

The optional state helper marks `SUSPECTED_STALL` after four **unchanged comparisons** beyond the first baseline observation. This is intentionally conservative and is not permission to terminate the run.
