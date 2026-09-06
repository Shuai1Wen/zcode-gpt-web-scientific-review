---
name: gpt-web-orchestrator
description: Orchestrate an independent scientific review through ChatGPT Web from ZCode. Use when a user asks for GPT Web review, second-model scientific review, blind review, Pro review, Extra High review, adversarial review, or evidence adjudication. Coordinates model routing, job state, browser review, heartbeat policy, result freezing, and final adjudication.
when_to_use: Use for deliberate low-frequency research review tasks where ChatGPT Web should act as an independent external reviewer rather than as an API backend.
license: MIT
metadata:
  version: 0.1.2
---

# GPT Web Scientific Review Orchestrator

## Objective

Run a scientifically useful independent review with the following invariant:

```text
independent packet -> external review -> freeze -> cross-examination -> evidence adjudication
```

Never collapse this into "ask ChatGPT what it thinks and copy the answer".

## Required companion skills

When the workflow reaches the corresponding phase, invoke/follow:

- `gpt-web-browser` for ChatGPT Web interaction. All browser work goes through ZCode's **in-app browser (IAB) backend**, reusing the user's existing chatgpt.com tab — never an external/spawned browser or an extra tab per job.
- `gpt-scientific-review` for packet and prompt construction.
- `gpt-pro-watch` when the selected model is Pro and the run may be long.
- `gpt-review-adjudicator` after the raw external review is frozen.

## Model policy

Only two execution classes are allowed:

- `EXTRA_HIGH`
- `PRO`

Never silently use Instant, Medium, High, Auto, or another lower class.

### Default routing

Choose `PRO` if any of the following is true:

1. The user explicitly requests Pro, final adjudication, final reconstruction, or publication-level terminal review.
2. The task asks whether the central scientific question is identifiable/answerable from the data.
3. A complete mathematical model, new algorithm, causal structure, or biological mechanism is being accepted/rejected.
4. Multiple plausible models disagree on a core claim.
5. The decision could force a major redesign of the project or manuscript.
6. The review must integrate multiple interacting layers: data-generating process, mathematics, algorithm, experiments, and claims.

Otherwise choose `EXTRA_HIGH` for focused section review, code alignment, a bounded formula check, a specific experiment interpretation, or a normal second opinion.

### No silent fallback

If the requested/selected class cannot be verified in the ChatGPT UI:

```text
status = MODEL_UNAVAILABLE
```

Do not submit to a lower class unless the user explicitly allowed fallback. Record any explicit fallback in `state.json`.

## Job workspace

Use a project-local directory, never the plugin installation directory:

```text
.gpt-web-review/
  coordinator.json
  jobs/<job-id>/
```

Recommended job id:

```text
YYYYMMDD_HHMM_<short-slug>
```

Create these artifacts as the workflow progresses:

```text
state.json
review_packet.md
prompt_blind.md
response_raw.md
prompt_challenge.md
challenge_raw.md
adjudication.md
```

Do not store credentials, cookies, browser tokens, authentication headers, 2FA material, or exported browser profiles.

## State machine

Valid primary states:

```text
CREATED
PACKET_READY
MODEL_SELECTED
SUBMITTED
RUNNING_PRO
RUNNING_XHIGH
COMPLETED
EXTRACTED
CHALLENGE_SUBMITTED
CHALLENGE_COMPLETED
ADJUDICATING
DONE
MODEL_UNAVAILABLE
AUTH_REQUIRED
RATE_LIMITED
BROWSER_LOST
SUSPECTED_STALL
FAILED
```

A terminal error-like state is not permission to auto-retry. Preserve evidence and report what happened.

## Phase 1 — Define the exact review target

Restate the review target as a falsifiable or adjudicable question. Examples:

- Does this model actually identify unseen-donor cell-state distributions from the provided context?
- Does the mathematical operator use observed response information or merely re-infer response from gene embeddings?
- Does the current manuscript support its claimed algorithmic novelty?

Separate:

- central scientific claim;
- required evidence;
- available evidence;
- constraints;
- requested verdict.

Do not turn local stability checks into the main scientific target.

## Phase 2 — Build a blind packet

Use `gpt-scientific-review`.

The packet must include sufficient facts for independent reasoning but remove anchoring from the current ZCode conclusion.

Do not include phrases such as:

- "ZCode thinks..."
- "we have decided..."
- "the previous reviewer prefers..."
- "the user wants method X to win..."

If the current implementation itself is evidence, include the implementation facts/code, but not the current evaluator's verdict.

Before submission, save `review_packet.md` and `prompt_blind.md`.

## Phase 3 — Open ChatGPT Web and verify model

Use `gpt-web-browser`.

Prefer a fresh Temporary Chat when practical for independence. If Temporary Chat is unavailable, create a new conversation with no project-specific prior messages.

Verify the visible model label after selection. Record exactly what is visible. Do not infer a hidden backend model from product announcements.

Only after verification set `MODEL_SELECTED` and submit.

## Phase 4 — Run and monitor

For `EXTRA_HIGH`, observe the browser until the response is clearly complete in the current interactive run.

For `PRO`:

1. set `RUNNING_PRO`;
2. ensure the Pro heartbeat protocol is configured;
3. return control to ZCode rather than repeatedly poking the page;
4. heartbeats inspect state only and must not send messages, refresh without cause, or click Stop/Retry.

Use `gpt-pro-watch` for every heartbeat.

## Phase 5 — Freeze raw result

When completion criteria are satisfied:

1. capture the external review verbatim enough to preserve its reasoning and verdict;
2. save it to `response_raw.md` before exposing ZCode's prior conclusion;
3. record `response_frozen=true` and a SHA-256 when practical;
4. set `EXTRACTED`.

Never silently rewrite the raw external response to make it agree with ZCode.

## Phase 6 — Adversarial comparison

Only after freezing, construct `prompt_challenge.md`.

Provide the reviewer with ZCode's current proposal/claim and ask it to compare against its blind review. The goal is not to ask for a fresh generic answer. Require explicit conflict-by-conflict analysis:

1. what the blind review said;
2. what the current ZCode proposal says;
3. what evidence supports each side;
4. whether the conflict changes the main scientific conclusion;
5. what exact modification follows.

Save the second response as `challenge_raw.md`.

## Phase 7 — Evidence adjudication

Use `gpt-review-adjudicator`.

ZCode must not accept GPT because it is GPT. Resolve each disagreement with evidence and classify it as:

```text
ACCEPT_GPT
REJECT_GPT
MODIFY_BOTH
UNRESOLVED
```

The final output should distinguish:

- core scientific changes;
- algorithm/model changes;
- experiment changes;
- supporting/robustness changes;
- engineering-only notes.

Main-line discipline for the final output: apply the adjudicator's main-line gate before presenting anything to the user. Lead with the 1-4 changes that act on the central claim's mechanism and the 1-3 experiments that can falsify it. Audit-grade suggestions (code hygiene, logging, seeds, completeness ablations, documentation) are never presented as review results — at most one aggregated "dropped as off-main-line" line. The deliverable is the smallest main-line fix, not an exhaustive findings report.

## Completion criteria

A review job is `DONE` only when:

- the blind packet exists;
- the requested model class was verified or an explicit fallback was recorded;
- the raw first response is frozen;
- any requested challenge phase is captured;
- adjudication is evidence-based;
- unresolved questions are explicit;
- the final recommendation returns to the original scientific objective;
- the final recommendation passed the main-line gate (no audit-grade items presented as results).

## Safety and service boundary

This workflow is for low-frequency, user-initiated review. Do not implement account rotation, rate-limit evasion, CAPTCHA bypass, bulk harvesting, or a high-throughput unofficial ChatGPT API.
