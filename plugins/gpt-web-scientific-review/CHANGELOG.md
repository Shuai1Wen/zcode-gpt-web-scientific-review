# Changelog

## 0.1.1 - 2026-09-06

- Pinned browser routing to ZCode's in-app browser (IAB backend, `agent.browsers.get("iab")`); explicitly forbade chrome-devtools MCP / cdp headless / OS-level browser automation, which do not share the user's ChatGPT login.
- Added a tab-reuse policy: reuse the existing chatgpt.com in-app tab (claim it when user-owned), navigate in place for every job stage, and only create one new tab when none exists. No extra tab/window per job.

## 0.1.0 - 2026-09-06

- Initial ZCode marketplace/plugin implementation.
- Added five core Skills and seven slash commands.
- Added Extra High / Pro-only model routing.
- Added blind-review packet construction and Temporary Chat preference.
- Added read-only Pro heartbeat state machine using two interleaved hourly tasks.
- Added raw-response freezing, adversarial comparison, and evidence adjudication.
- Added state helper, package validator, tests, and Windows installation guidance.
