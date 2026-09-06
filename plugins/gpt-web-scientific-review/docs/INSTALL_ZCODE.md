# Install in ZCode

This project is packaged as a ZCode **marketplace containing one plugin**.

## Requirements

- ZCode desktop build with Plugins, Skills, Commands, Browser Automation, and Automations.
- A normal ChatGPT Web account/session that exposes the reasoning mode you intend to use.
- Python 3.10+ only if you want to use the optional local state helper/tests. The Skills themselves do not require Python.

## 1. Install the marketplace

Extract the project to a stable local folder. The root must contain:

```text
marketplace.json
plugins/
```

In ZCode:

1. Open **Settings -> Plugins**.
2. Choose **Create -> Add marketplace**.
3. Select the extracted repository root (not only the plugin subfolder).
4. Find `gpt-web-scientific-review` under the Personal marketplace.
5. Install and enable it.
6. Confirm five Skills and seven Commands appear in the plugin details.

After modifying the source locally, refresh the custom marketplace before retesting.

## 2. Confirm Browser Automation

ZCode's official Browser Automation / Browser Use capability should be enabled. The plugin does not ship a custom browser driver and does not use Playwright or an OpenAI API endpoint.

## 3. First ChatGPT Web login

Run:

```text
/gpt-review-setup
```

The setup flow opens `https://chatgpt.com/` in ZCode's built-in browser.

If login, CAPTCHA, 2FA, email verification, or another security prompt appears, complete it yourself in the visible browser. The plugin must not store or extract credentials.

### Windows note

Treat ZCode's browser session as independent from your Chrome browser unless your exact ZCode build explicitly exposes a supported import mechanism. The safest assumption is: log in once inside ZCode's own browser and keep that session.

## 4. Configure Pro heartbeat tasks

`/gpt-review-setup` asks ZCode to create two session-bound scheduled tasks when the current build exposes scheduled-task creation from chat:

- Hourly at minute **00**
- Hourly at minute **30**

Together they approximate a 30-minute heartbeat while using only ZCode's supported hourly recurrence.

If automatic creation is unavailable, create the two tasks manually using `docs/HEARTBEAT_SETUP.md`.

## 5. Enable Keep awake

For long Pro jobs, open ZCode **Automations** and enable the global **Keep awake** switch. Scheduled tasks run on the local computer, so ZCode must remain running and the machine must remain awake.

## 6. Smoke test

Start with a bounded Extra High job:

```text
/gpt-review-xhigh Check whether this toy mathematical objective matches the stated estimand: ...
```

Confirm that:

1. `.gpt-web-review/jobs/<job-id>/` is created;
2. a fresh ChatGPT conversation is used;
3. the visible Extra High mode is verified before submission;
4. `review_packet.md` and `prompt_blind.md` are saved;
5. the raw response is frozen before adjudication.

Then test a Pro job only after the heartbeat setup is ready.
