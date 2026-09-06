# Changelog

## 0.1.2 - 2026-09-06

- Added a hard "main-line discipline" block to the blind-review contract (skill + template): section H may only contain changes acting on the central claim's mechanism, section I only claim-falsifying experiments; audit-grade work (code audits, logging, seeds, hyperparameter hygiene, completeness ablations, documentation, checklists) is forbidden in H/I; H normally 1-4 changes, I 1-3 experiments.
- Packet builder rule: section 8 questions must each be capable of changing the verdict or the main-method design.
- Challenge prompt now carries the same main-line discipline.
- Adjudicator: new main-line gate — an item enters "Core method changes"/"Core experiments" only if resolving it can change the verdict; audit-grade items are dropped to a single aggregated "Dropped as off-main-line" line; artifact sections annotated accordingly.
- Orchestrator: final output must lead with main-line changes and never present audit-grade items as review results; added to completion criteria.

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
