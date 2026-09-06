---
name: gpt-web-browser
description: Drive ZCode's built-in browser for a single ChatGPT Web scientific-review job. Use when the orchestrator needs to open chatgpt.com, verify login, create a clean review conversation, select Extra High or Pro, submit a review prompt, inspect generation state, or extract a completed response without using the OpenAI API.
when_to_use: Use only for interactive, low-frequency ChatGPT Web review jobs initiated by the user.
license: MIT
metadata:
  version: 0.1.1
---

# GPT Web Browser Protocol

## Hard boundary

Use ZCode's official built-in Browser Automation/Browser Use capability — and specifically the **in-app browser (IAB) backend**: after the standard browser-use bootstrap, select it with `agent.browsers.get("iab")`.

Do NOT drive any external or separately launched browser for this workflow:

- no chrome-devtools MCP tools (they attach to a different Chrome instance that does not share the user's ChatGPT login);
- no `cdp`/headless managed browser;
- no OS-level window automation against Chrome/Edge;
- no unofficial HTTP endpoint, cookie replay, hidden API call, or automated credential extraction.

Only the in-app browser carries the user's manually authenticated ChatGPT Web session.

The browser UI is dynamic. Prefer semantic interaction driven by the ARIA/DOM snapshot (`tab.playwright.domSnapshot()` → role/text locators) over hard-coded CSS selectors.

## In-app browser tab policy

Never open an extra browser window or tab merely to run a review. The user's in-app browser tab IS the review surface:

1. After selecting the IAB backend, read `browser.tabs.list()` AND `browser.user.openTabs()`.
2. If any `chatgpt.com` tab already exists (controlled or user tab), reuse it: `browser.tabs.get(id)` for a controlled tab, `browser.user.claimTab(info)` for a user tab. Never create a duplicate tab when one exists.
3. Only when NO chatgpt.com tab exists at all, create exactly one with `browser.tabs.new()` (this also reveals the browser pane for the user).
4. Every job stage happens by **navigating in place inside that single tab**: fresh chat (`https://chatgpt.com/`), Temporary Chat (via the visible UI control), submission, monitoring, challenge phase. Do not stack one new tab per job.
5. Preserve this tab across jobs and heartbeats; closing it is never part of a job and forfeits Temporary-Chat recovery.
6. Navigating the tab away from an existing conversation is safe for the user: ChatGPT keeps all conversations in history, reachable from the sidebar.

## Authentication

1. Reuse or open `https://chatgpt.com/` in the single in-app browser tab per the tab policy above.
2. Determine whether the user is already logged in.
3. If password, CAPTCHA, 2FA, email verification, payment, or other security verification is required:
   - set `AUTH_REQUIRED`;
   - tell the user exactly what must be completed manually;
   - do not request, read, save, or type secrets on the user's behalf unless ZCode's normal interactive UI explicitly leaves that action to the user.
4. Resume only after the authenticated ChatGPT page is visibly available.

On Windows, assume the ZCode browser session is distinct from Chrome unless the current ZCode build explicitly indicates otherwise.

## Conversation isolation

For a blind review, prefer:

1. Temporary Chat, if the visible UI offers it; otherwise
2. a new empty conversation.

Do not reuse an old project conversation for the initial blind review. A "fresh conversation" means navigating the SAME in-app tab to a new chat / Temporary Chat, not opening another tab.

If Temporary Chat is used, record `temporary_chat=true`. Be aware that losing the tab may make recovery harder; preserve the tab during long Pro runs.

## Model selection

Accepted requested modes:

```text
EXTRA_HIGH
PRO
```

### Selection procedure

1. Inspect the current model/mode control.
2. Open it and select the exact requested class exposed in the UI.
3. Close the selector if needed.
4. Re-read the composer/header area and verify the visible current label.
5. Record the literal UI label in `visible_model`.

Examples:

```text
requested_mode = PRO
visible_model = "Pro"
backend_model = "UNKNOWN"
```

or, if the UI explicitly shows a model name:

```text
visible_model = "GPT-6 Pro"
backend_model = "GPT-6 Pro"
```

Never infer a hidden model name from release notes. If the class cannot be verified, set `MODEL_UNAVAILABLE` and do not submit.

## Prompt submission

Before submitting:

- confirm the prompt begins with the blind-review instructions;
- confirm it does not reveal ZCode's current verdict during Phase A;
- confirm the task contains the central question, supplied evidence, constraints, and required output schema;
- avoid sending unnecessary sensitive or identifying data.

Submit exactly once. Record the conversation URL if one is available without exposing authentication material.

Set:

```text
SUBMITTED
```

then:

```text
RUNNING_PRO
```

or

```text
RUNNING_XHIGH
```

## Completion detection

Do not declare completion merely because partial text is visible.

Use multiple visible signals. A robust completion determination requires all of the following when the UI supports them:

1. no active generation/thinking/working indicator;
2. no active Stop control associated with generation;
3. composer is available for a new message;
4. a non-empty assistant response exists;
5. the final assistant response appears stable across a second observation.

If one signal is ambiguous, keep the job running rather than interrupting it.

## Pro long-run rules

During a Pro run, never automatically:

- click Stop;
- click Retry;
- send "continue";
- resend the prompt;
- refresh merely because the task is taking a long time;
- switch to Extra High;
- create a duplicate chat;
- open multiple equivalent Pro requests.

A heartbeat is an observation, not a message to ChatGPT.

## Error states

Set a specific state only when there is visible evidence:

- `AUTH_REQUIRED`: login/security interaction needed.
- `RATE_LIMITED`: UI explicitly indicates rate/usage limitation.
- `BROWSER_LOST`: the relevant tab is gone and cannot be recovered from a stored non-secret URL.
- `MODEL_UNAVAILABLE`: requested model class cannot be selected/verified.
- `FAILED`: explicit unrecoverable page/request failure.

A long unchanged Pro run is not automatically `FAILED`; use `SUSPECTED_STALL` after repeated unchanged heartbeats while preserving the tab.

## Extraction and freeze

When completion is verified:

1. collect the final assistant response in its original structure;
2. preserve equations, tables, verdict labels, caveats, and citations/links that are part of the response;
3. write `response_raw.md` before sending any challenge prompt;
4. record extraction time and freeze status;
5. only then allow the orchestrator to expose ZCode's current conclusion.

Do not use the ChatGPT "Copy" button if another direct semantic read of the visible response is safer; either is acceptable if it preserves the response accurately.
