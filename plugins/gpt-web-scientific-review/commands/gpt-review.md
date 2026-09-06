---
description: Run an independent blind scientific review through ChatGPT Web, automatically routing only to Extra High or Pro.
argument-hint: "<scientific question, method, manuscript section, code path, or review target>"
skills: gpt-web-orchestrator, gpt-scientific-review, gpt-web-browser, gpt-pro-watch, gpt-review-adjudicator
disable-noninteractive: true
---

Run the complete GPT Web Scientific Review workflow for:

$ARGUMENTS

Requirements:

1. Treat ChatGPT Web as an independent external reviewer, not as an authority.
2. Route only to `EXTRA_HIGH` or `PRO` using the orchestrator's rules.
3. Build and save a blind `review_packet.md` and `prompt_blind.md` before opening the reviewer to ZCode's current verdict.
4. Use ZCode's built-in browser and the user's manually authenticated ChatGPT Web session. Do not use the OpenAI API or hidden endpoints.
5. Verify the visible requested model class after selection. Never silently downgrade.
6. Prefer a fresh Temporary Chat for the blind phase when the UI offers it.
7. For Pro, use the read-only heartbeat protocol; do not poke or interrupt a long-running review.
8. Freeze the raw first response before any adversarial comparison.
9. If appropriate, run the challenge phase, then adjudicate conflicts by evidence.
10. Preserve the main scientific question and distinguish CORE, SUPPORTING, ROBUSTNESS, and ENGINEERING issues.

If authentication or a security challenge requires the user, set `AUTH_REQUIRED` and stop browser automation at that point.
