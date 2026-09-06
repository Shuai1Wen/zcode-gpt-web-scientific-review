# Optional State Helper

The workflow can maintain JSON files directly through ZCode. `scripts/job_state.py` is an optional dependency-free helper for reproducible local state changes.

Run from your research project root, specifying the helper by path, or copy the script into your tooling directory.

## Initialize coordinator metadata

```bash
python job_state.py --root . setup
```

## Create a Pro job

```bash
python job_state.py --root . new --topic "unseen donor final review" --mode PRO
```

## Record model verification and state

```bash
python job_state.py --root . set <job-id> MODEL_SELECTED --visible-model "Pro" --temporary-chat true
python job_state.py --root . set <job-id> RUNNING_PRO --chat-url "https://chatgpt.com/..."
```

`backend_model` should remain `UNKNOWN` unless the visible UI explicitly identifies it.

## Record heartbeat

```bash
python job_state.py --root . heartbeat <job-id> --summary "thinking indicator visible" --result running
```

Supported results:

```text
running
completed
auth
rate_limited
browser_lost
```

## Freeze external response

First save the extracted response to a temporary Markdown file, then:

```bash
python job_state.py --root . freeze <job-id> --file extracted.md
```

The helper writes/locks `response_raw.md`, records SHA-256, and advances the state to `EXTRACTED` where appropriate. It refuses to overwrite different content unless `--force` is deliberately used.

## Show/list

```bash
python job_state.py --root . show <job-id>
python job_state.py --root . list
```

## Credential safety

The helper rejects suspicious JSON key names such as password, cookie, session token, authorization token, TOTP/2FA material, recovery code, and API key. This is a guardrail, not a complete secret scanner.
