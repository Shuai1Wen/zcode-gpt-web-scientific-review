# Troubleshooting

## Plugin does not appear

Check:

1. You added the repository root containing `marketplace.json`, not an arbitrary nested directory.
2. `marketplace.json` points to `./plugins/gpt-web-scientific-review`.
3. `.zcode-plugin/plugin.json` exists.
4. Refresh the custom marketplace after source changes.
5. Run `python scripts/validate_plugin.py` from the plugin directory.

## Skill visible but not triggered automatically

Invoke the slash command directly or select the Skill explicitly. Disable unrelated Skills if your ZCode installation has a very large enabled-skill set, because enabled Skill metadata shares a context budget.

## Browser cannot access ChatGPT session

Open ChatGPT Web manually in ZCode's built-in browser. Complete login/security verification yourself. Do not attempt cookie extraction or browser-profile workarounds.

## Pro is not visible

Set `MODEL_UNAVAILABLE`. Do not silently run Extra High unless the user explicitly changes the request or allows fallback.

## UI shows only "Pro" and not a backend model name

Record:

```text
visible_model = Pro
backend_model = UNKNOWN
```

Do not infer a hidden model name.

## Pro seems stuck

Do not click Stop/Retry automatically. Heartbeats should continue read-only. After repeated unchanged observations the job may be marked `SUSPECTED_STALL`; a human then decides whether any destructive recovery is justified.

## Temporary Chat tab was closed

If the conversation cannot be recovered normally, mark `BROWSER_LOST`. Do not try to reconstruct the session from cookies/tokens. A new blind review is a new job and should be recorded as such.

## Scheduled heartbeat did not run

Check:

- ZCode was running;
- the computer was awake;
- Keep awake was enabled for unattended long runs;
- the two tasks are active;
- they target the local project/coordinator session.

A missed heartbeat is not evidence that ChatGPT stopped.

## Raw response accidentally changed

The optional helper's `freeze` command refuses to overwrite a different `response_raw.md` unless `--force` is supplied. Prefer restoring the frozen version and its recorded SHA-256 rather than editing it.
