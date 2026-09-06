# ZCode GPT Web Scientific Review

A ZCode plugin that uses **ZCode's built-in Browser Automation** to open the user's existing ChatGPT Web session and run an **independent scientific review**. It does **not** use the OpenAI API and is intentionally designed as a low-frequency, human-initiated review workflow rather than a bulk scraping backend.

## Core workflow

```text
ZCode main agent
    |
    v
/gpt-review, /gpt-review-xhigh, /gpt-review-pro
    |
    v
Blind review packet builder
    |
    v
ZCode Browser -> chatgpt.com -> Extra High or Pro
    |
    +-- Pro: read-only heartbeat every ~30 min (:00 + :30 hourly tasks)
    |
    v
Freeze raw GPT review
    |
    v
Adversarial comparison
    |
    v
Evidence-based ZCode adjudication
```

## What is included

- 5 focused Skills
- 7 slash commands
- Extra High / Pro-only routing
- blind review packets that remove anchoring from ZCode's current conclusion
- Temporary Chat preference for independence
- Pro long-run heartbeat protocol
- explicit `MODEL_UNAVAILABLE`, `AUTH_REQUIRED`, `RATE_LIMITED`, and `SUSPECTED_STALL` states
- frozen raw review artifacts before any cross-examination
- conflict-matrix adjudication (`ACCEPT_GPT`, `REJECT_GPT`, `MODIFY_BOTH`, `UNRESOLVED`)
- an optional dependency-free Python state helper and tests
- Windows-focused installation and first-login notes

## Install

### From GitHub (recommended)

1. In ZCode open **Settings -> Plugins -> Create -> Add marketplace** (插件市场 -> 添加插件市场).
2. Paste the repository URL: `https://github.com/Shuai1Wen/zcode-gpt-web-scientific-review`
3. In the Personal marketplace, install and enable **gpt-web-scientific-review**.
4. Continue with the common steps below.

### From a local copy

1. Clone or extract this repository to a stable local path.
2. In ZCode open **Settings -> Plugins -> Create -> Add marketplace**.
3. Choose the repository root (the directory containing `marketplace.json`).
4. In the Personal marketplace, install and enable **gpt-web-scientific-review**.
5. Continue with the common steps below.

### Common steps

1. Confirm the official **Browser Use / Browser Automation** capability is enabled. Browser work must go through ZCode's **in-app browser (IAB backend)**, reusing the logged-in chatgpt.com tab — never an external/spawned browser (v0.1.1+ hard rule).
2. Run `/gpt-review-setup` once in the coordinator session.
3. In ZCode's built-in browser, open `https://chatgpt.com/` and log in manually. Complete passwords and 2FA yourself.

See `plugins/gpt-web-scientific-review/docs/INSTALL_ZCODE.md` for details.

## Primary commands

```text
/gpt-review <research question or artifact to review>
/gpt-review-xhigh <task>
/gpt-review-pro <task>
/gpt-review-status [job id]
/gpt-review-resume [job id]
/gpt-review-collect [job id]
/gpt-review-setup
```

`/gpt-review` routes only to **Extra High** or **Pro**. It must never silently downgrade a requested Pro run.

## Design boundary

This plugin treats ChatGPT Web as an **external reviewer**, not as an authority. ZCode must preserve the raw response before showing the reviewer ZCode's own conclusion, then adjudicate disagreements using evidence.

Do not use this project to create a high-throughput unofficial API, automate account switching, bypass rate limits, or harvest large quantities of ChatGPT output.

## Project state

Each project may use:

```text
.gpt-web-review/
  coordinator.json
  jobs/
    <job-id>/
      state.json
      review_packet.md
      prompt_blind.md
      response_raw.md
      prompt_challenge.md
      challenge_raw.md
      adjudication.md
```

The plugin instructions explicitly prohibit storing passwords, cookies, session tokens, 2FA secrets, or authentication headers in these files.

## Validate the package

From the plugin directory:

```bash
python scripts/validate_plugin.py
python -m unittest discover -s tests -v
```

## License

MIT. See `LICENSE`.
