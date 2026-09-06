#!/usr/bin/env python3
"""Static validator for the packaged ZCode plugin/marketplace."""
from __future__ import annotations

import json
import re
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
PLUGIN = HERE.parent
MARKET = PLUGIN.parent.parent

PLUGIN_NAME_RE = re.compile(r'^[a-z0-9][a-z0-9._-]{0,127}$')
COMMAND_NAME_RE = re.compile(r'^[a-z0-9][a-z0-9_:-]{0,63}$')


def frontmatter(path: Path) -> dict[str, str]:
    text = path.read_text(encoding='utf-8')
    if not text.startswith('---\n'):
        raise ValueError(f'{path}: missing YAML frontmatter')
    end = text.find('\n---\n', 4)
    if end < 0:
        raise ValueError(f'{path}: unterminated YAML frontmatter')
    out: dict[str, str] = {}
    for line in text[4:end].splitlines():
        if not line.strip() or line.startswith(' ') or ':' not in line:
            continue
        k, v = line.split(':', 1)
        out[k.strip()] = v.strip().strip('"\'')
    return out


def main() -> int:
    errors: list[str] = []
    try:
        manifest = json.loads((PLUGIN / '.zcode-plugin/plugin.json').read_text(encoding='utf-8'))
        name = manifest.get('name', '')
        if not PLUGIN_NAME_RE.fullmatch(name):
            errors.append(f'invalid plugin name: {name!r}')
        if manifest.get('commands') != 'commands':
            errors.append('manifest commands should be "commands"')
        if manifest.get('skills') != 'skills':
            errors.append('manifest skills should be "skills"')
    except Exception as e:
        errors.append(f'plugin.json: {e}')

    try:
        marketplace = json.loads((MARKET / 'marketplace.json').read_text(encoding='utf-8'))
        entries = [x for x in marketplace.get('plugins', []) if x.get('name') == 'gpt-web-scientific-review']
        if len(entries) != 1:
            errors.append('marketplace must contain exactly one gpt-web-scientific-review entry')
        elif entries[0].get('version') != manifest.get('version'):
            errors.append('marketplace and plugin versions differ')
    except Exception as e:
        errors.append(f'marketplace.json: {e}')

    skill_dirs = sorted((PLUGIN / 'skills').glob('*'))
    if len(skill_dirs) != 5:
        errors.append(f'expected 5 skills, found {len(skill_dirs)}')
    for d in skill_dirs:
        f = d / 'SKILL.md'
        if not f.is_file():
            errors.append(f'missing {f}')
            continue
        try:
            fm = frontmatter(f)
            if fm.get('name') != d.name:
                errors.append(f'{f}: frontmatter name must match directory')
            desc = fm.get('description', '')
            if not desc:
                errors.append(f'{f}: missing description')
            if len(desc) > 1024:
                errors.append(f'{f}: description exceeds 1024 chars')
            if len(f.read_bytes()) > 100 * 1024:
                errors.append(f'{f}: body/file exceeds 100KB load limit')
        except Exception as e:
            errors.append(str(e))

    commands = sorted((PLUGIN / 'commands').glob('*.md'))
    if len(commands) != 7:
        errors.append(f'expected 7 commands, found {len(commands)}')
    skill_names = {d.name for d in skill_dirs}
    for f in commands:
        if not COMMAND_NAME_RE.fullmatch(f.stem):
            errors.append(f'invalid command name: {f.stem}')
        try:
            fm = frontmatter(f)
            if not fm.get('description'):
                errors.append(f'{f}: missing description')
            for skill in [s.strip() for s in fm.get('skills', '').split(',') if s.strip()]:
                if skill not in skill_names:
                    errors.append(f'{f}: references unknown skill {skill}')
        except Exception as e:
            errors.append(str(e))

    if errors:
        print('VALIDATION FAILED')
        for e in errors:
            print('-', e)
        return 1
    print('VALIDATION OK')
    print(f'plugin={manifest["name"]} version={manifest["version"]}')
    print(f'skills={len(skill_dirs)} commands={len(commands)}')
    return 0


if __name__ == '__main__':
    sys.exit(main())
