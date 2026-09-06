# Validation Report — 2026-09-06

## Scope

This report validates the distributable project structure and dependency-free local state helper. The current execution environment does **not** contain the ZCode desktop GUI, so live ChatGPT Web UI interaction is not claimed as end-to-end GUI-tested.

## ZCode schema checks

Validated against the current ZCode plugin/skill/command documentation available on 2026-09-06:

- marketplace root contains `marketplace.json`;
- plugin lives at `plugins/gpt-web-scientific-review`;
- manifest is at `.zcode-plugin/plugin.json`;
- manifest plugin name matches ZCode naming constraints;
- Skills are flat at `skills/<name>/SKILL.md`;
- each Skill has `name` and `description` frontmatter;
- Skill descriptions are below the 1024-character limit;
- Skill files are below the 100 KB loading limit;
- Commands are in `commands/*.md` with frontmatter;
- command-declared Skills resolve to packaged Skill names;
- marketplace/plugin versions match.

Result:

```text
VALIDATION OK
plugin=gpt-web-scientific-review version=0.1.0
skills=5 commands=7
```

## Python tests

Commands run:

```bash
python -m py_compile scripts/job_state.py scripts/validate_plugin.py
python -m unittest discover -s tests -v
```

Result:

```text
Ran 10 tests
OK
```

Covered behaviors:

1. coordinator setup;
2. new-job creation;
3. forward state transition;
4. accidental backward transition rejection;
5. Pro heartbeat counting;
6. conservative `SUSPECTED_STALL` threshold;
7. response freezing and SHA-256 recording;
8. refusal to overwrite a different frozen raw response by default;
9. sensitive-key detection;
10. marketplace/manifest/Skill/Command structure.

## CLI dry run

A temporary project was exercised through:

```text
CREATED
-> PACKET_READY
-> MODEL_SELECTED (visible_model=Pro)
-> RUNNING_PRO
-> heartbeat STILL_RUNNING
-> heartbeat COMPLETED
-> EXTRACTED
```

`response_raw.md` was frozen and a SHA-256 digest was persisted.

## Not claimed as tested here

The following require the user's real ZCode desktop application and ChatGPT account/UI:

- actual ZCode marketplace installation UI;
- live Browser Automation interaction with chatgpt.com;
- exact current model-menu labels on the user's account;
- Temporary Chat availability on the user's account;
- live creation of the two session-bound ZCode scheduled heartbeat tasks;
- long-running Pro completion behavior.

The Skills therefore avoid fixed CSS selectors, record literal visible model labels, refuse silent fallback, and classify unsupported/ambiguous UI states explicitly.
