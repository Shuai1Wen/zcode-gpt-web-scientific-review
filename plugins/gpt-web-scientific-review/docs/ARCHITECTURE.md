# Architecture

## Design objective

The project is an **independent-review coordinator**, not a ChatGPT wrapper.

```text
                 ZCode main agent
                       |
                /gpt-review*
                       |
             gpt-web-orchestrator
                 /            \
                v              v
   gpt-scientific-review   model router
                |              |
                +------> EXTRA_HIGH / PRO
                               |
                               v
                      gpt-web-browser
                               |
                         ChatGPT Web
                               |
                    +----------+----------+
                    |                     |
                 xhigh                  pro
                    |                     |
                    |              gpt-pro-watch
                    |               :00 / :30
                    +----------+----------+
                               |
                         freeze raw result
                               |
                     adversarial comparison
                               |
                  gpt-review-adjudicator
                               |
                          final decision
```

## Why five Skills

ZCode injects metadata for enabled Skills into the model context. A small number of precise Skills is therefore preferable to dozens of narrow ones.

### `gpt-web-orchestrator`

Owns the end-to-end state machine, routing, artifacts, and completion criteria.

### `gpt-web-browser`

Owns only visible ChatGPT Web interaction: login checks, clean conversation, mode selection, submission, completion detection, extraction.

### `gpt-scientific-review`

Owns scientific packet construction, anti-anchoring rules, review axes, blind prompt, and challenge prompt.

### `gpt-pro-watch`

Owns long Pro monitoring. It is deliberately read-only.

### `gpt-review-adjudicator`

Owns the evidence-based conflict matrix and final reconstruction.

## Persistent project state

State is project-local:

```text
.gpt-web-review/
  coordinator.json
  jobs/
    20260906_1730_example/
      state.json
      review_packet.md
      prompt_blind.md
      response_raw.md
      prompt_challenge.md
      challenge_raw.md
      adjudication.md
```

This allows ZCode to resume after a session interruption without resubmitting the external review.

## State machine

```text
CREATED
  -> PACKET_READY
  -> MODEL_SELECTED
  -> SUBMITTED
  -> RUNNING_XHIGH | RUNNING_PRO
  -> COMPLETED
  -> EXTRACTED
  -> CHALLENGE_SUBMITTED (optional)
  -> CHALLENGE_COMPLETED (optional)
  -> ADJUDICATING
  -> DONE
```

Blocking/recovery states:

```text
MODEL_UNAVAILABLE
AUTH_REQUIRED
RATE_LIMITED
BROWSER_LOST
SUSPECTED_STALL
FAILED
```

The state helper permits recovery from blocking states but refuses ordinary backwards movement unless explicitly forced.

## Independence mechanism

The most important architectural property is ordering:

```text
1. Build factual packet
2. Remove ZCode verdict
3. Run blind external review
4. Freeze raw external review
5. Only then reveal ZCode position
6. Cross-examine
7. Adjudicate with evidence
```

This reduces confirmation/anchoring effects compared with asking a second model to "review the answer above".

## No hidden backend assumptions

The browser Skill records the literal visible model label. If the UI says `Pro`, it records `Pro`; it does not infer a hidden backend model name from announcements or prior knowledge.

## No unofficial API layer

The architecture intentionally omits:

- custom HTTP calls to ChatGPT internal endpoints;
- cookie replay;
- browser-profile extraction;
- account rotation;
- bulk request queues;
- CAPTCHA/rate-limit bypass.

This keeps the project focused on user-initiated scientific review.
