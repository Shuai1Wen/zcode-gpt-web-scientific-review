# Design Decisions

## 1. Plugin, not loose Skills

A plugin gives one installable unit while still keeping five narrowly defined Skills and reusable slash commands.

## 2. No custom MCP/browser driver in v0.1

ZCode already supplies Browser Automation. Adding Playwright or an MCP server would duplicate capability and increase security/maintenance surface.

## 3. Extra High and Pro only

The workflow is intended for independent scientific review rather than cheap general chat. Model selection is therefore binary and explicit.

## 4. No silent fallback

A hidden downgrade would invalidate the review record. `MODEL_UNAVAILABLE` is preferable to pretending a Pro review occurred.

## 5. Two hourly heartbeat tasks

ZCode scheduling exposes Hour as the smallest repeat unit. Two session-bound tasks at :00 and :30 implement the requested ~30-minute cadence without relying on unsupported cron syntax.

## 6. Heartbeat is observational

Long reasoning should not be interrupted. A heartbeat never messages ChatGPT and never uses elapsed time alone as a failure signal.

## 7. Blind first, challenge second

This is the core anti-anchoring mechanism. The first response is frozen before ZCode's existing conclusion is shown.

## 8. Evidence adjudication, not voting

The final result is not "two models agree". Each conflict is classified by evidence and scientific level.

## 9. Project-local artifacts

Keeping `.gpt-web-review` in the research workspace makes the review reproducible and resumable without embedding credentials in the plugin.

## 10. No high-throughput web backend

The project deliberately excludes account rotation, scraping queues, hidden endpoints, and access-control circumvention. Its intended unit is a deliberate human-initiated review job.
