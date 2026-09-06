#!/usr/bin/env python3
"""Dependency-free state helper for GPT Web Scientific Review jobs.

This helper is optional: ZCode can maintain the same JSON state directly. It is
provided to make transitions, heartbeat counters, and raw-response freezing
repeatable from a local terminal without storing browser credentials.
"""
from __future__ import annotations

import argparse
import datetime as dt
import hashlib
import json
import os
import re
import sys
from pathlib import Path
from typing import Any

VALID_STATES = {
    'CREATED', 'PACKET_READY', 'MODEL_SELECTED', 'SUBMITTED',
    'RUNNING_PRO', 'RUNNING_XHIGH', 'COMPLETED', 'EXTRACTED',
    'CHALLENGE_SUBMITTED', 'CHALLENGE_COMPLETED', 'ADJUDICATING', 'DONE',
    'MODEL_UNAVAILABLE', 'AUTH_REQUIRED', 'RATE_LIMITED', 'BROWSER_LOST',
    'SUSPECTED_STALL', 'FAILED',
}

# Deliberately permissive around recovery states. The purpose is to prevent
# accidental backwards movement through successful phases, not to encode UI
# behavior that can change over time.
RANK = {
    'CREATED': 0,
    'PACKET_READY': 1,
    'MODEL_SELECTED': 2,
    'SUBMITTED': 3,
    'RUNNING_PRO': 4,
    'RUNNING_XHIGH': 4,
    'COMPLETED': 5,
    'EXTRACTED': 6,
    'CHALLENGE_SUBMITTED': 7,
    'CHALLENGE_COMPLETED': 8,
    'ADJUDICATING': 9,
    'DONE': 10,
}
RECOVERY_STATES = {
    'MODEL_UNAVAILABLE', 'AUTH_REQUIRED', 'RATE_LIMITED', 'BROWSER_LOST',
    'SUSPECTED_STALL', 'FAILED',
}
SECRET_KEYS = re.compile(
    r'(password|passwd|cookie|session[_-]?token|authorization|auth[_-]?token|'
    r'totp|2fa|recovery[_-]?code|api[_-]?key)', re.I
)


def now_iso() -> str:
    return dt.datetime.now(dt.timezone.utc).astimezone().isoformat(timespec='seconds')


def atomic_json(path: Path, data: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    tmp = path.with_suffix(path.suffix + '.tmp')
    tmp.write_text(json.dumps(data, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    os.replace(tmp, path)


def load_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding='utf-8'))


def project_dir(root: str | Path) -> Path:
    return Path(root).resolve() / '.gpt-web-review'


def job_dir(root: str | Path, job_id: str) -> Path:
    return project_dir(root) / 'jobs' / job_id


def state_path(root: str | Path, job_id: str) -> Path:
    return job_dir(root, job_id) / 'state.json'


def slugify(text: str) -> str:
    text = re.sub(r'[^a-zA-Z0-9_-]+', '-', text.strip()).strip('-_').lower()
    return (text or 'review')[:48]


def make_job_id(topic: str) -> str:
    stamp = dt.datetime.now().strftime('%Y%m%d_%H%M')
    return f'{stamp}_{slugify(topic)}'


def scan_secrets(obj: Any, prefix: str = '') -> list[str]:
    findings: list[str] = []
    if isinstance(obj, dict):
        for key, value in obj.items():
            key_path = f'{prefix}.{key}' if prefix else str(key)
            if SECRET_KEYS.search(str(key)):
                findings.append(key_path)
            findings.extend(scan_secrets(value, key_path))
    elif isinstance(obj, list):
        for i, value in enumerate(obj):
            findings.extend(scan_secrets(value, f'{prefix}[{i}]'))
    return findings


def cmd_setup(args: argparse.Namespace) -> int:
    base = project_dir(args.root)
    coord = base / 'coordinator.json'
    if coord.exists() and not args.force:
        print(coord)
        return 0
    data = {
        'schema_version': 1,
        'heartbeat_protocol': 'dual-hourly',
        'heartbeat_a_minute': 0,
        'heartbeat_b_minute': 30,
        'keep_awake_required': True,
        'created_at': now_iso(),
        'notes': args.notes or '',
    }
    atomic_json(coord, data)
    print(coord)
    return 0


def cmd_new(args: argparse.Namespace) -> int:
    mode = args.mode.upper()
    if mode not in {'PRO', 'EXTRA_HIGH'}:
        raise SystemExit('mode must be PRO or EXTRA_HIGH')
    jid = args.job_id or make_job_id(args.topic)
    path = state_path(args.root, jid)
    if path.exists() and not args.force:
        raise SystemExit(f'job already exists: {jid}')
    data = {
        'schema_version': 1,
        'job_id': jid,
        'topic': args.topic,
        'status': 'CREATED',
        'requested_mode': mode,
        'allow_fallback': bool(args.allow_fallback),
        'visible_model': None,
        'backend_model': 'UNKNOWN',
        'temporary_chat': None,
        'chat_url': None,
        'created_at': now_iso(),
        'submitted_at': None,
        'completed_at': None,
        'last_heartbeat_at': None,
        'heartbeat_count': 0,
        'unchanged_heartbeats': 0,
        'last_heartbeat_summary': None,
        'response_frozen': False,
        'response_sha256': None,
        'notes': [],
        'history': [{'at': now_iso(), 'event': 'created', 'status': 'CREATED'}],
    }
    atomic_json(path, data)
    print(jid)
    return 0


def ensure_transition(old: str, new: str, force: bool) -> None:
    if new not in VALID_STATES:
        raise SystemExit(f'invalid state: {new}')
    if force or old == new or new in RECOVERY_STATES or old in RECOVERY_STATES:
        return
    if old in RANK and new in RANK and RANK[new] >= RANK[old]:
        return
    raise SystemExit(f'refusing backwards transition {old} -> {new}; use --force only after manual review')


def cmd_set(args: argparse.Namespace) -> int:
    path = state_path(args.root, args.job_id)
    data = load_json(path)
    old = data['status']
    new = args.status.upper()
    ensure_transition(old, new, args.force)
    data['status'] = new
    if args.visible_model is not None:
        data['visible_model'] = args.visible_model
    if args.backend_model is not None:
        data['backend_model'] = args.backend_model
    if args.temporary_chat is not None:
        data['temporary_chat'] = args.temporary_chat == 'true'
    if args.chat_url is not None:
        data['chat_url'] = args.chat_url
    if new in {'SUBMITTED', 'RUNNING_PRO', 'RUNNING_XHIGH'} and not data.get('submitted_at'):
        data['submitted_at'] = now_iso()
    if new in {'COMPLETED', 'EXTRACTED', 'DONE'} and not data.get('completed_at'):
        data['completed_at'] = now_iso()
    if args.note:
        data.setdefault('notes', []).append(args.note)
    data.setdefault('history', []).append({'at': now_iso(), 'event': 'transition', 'from': old, 'status': new})
    findings = scan_secrets(data)
    if findings:
        raise SystemExit('refusing to write possible secret fields: ' + ', '.join(findings))
    atomic_json(path, data)
    print(new)
    return 0


def cmd_heartbeat(args: argparse.Namespace) -> int:
    path = state_path(args.root, args.job_id)
    data = load_json(path)
    if data['status'] not in {'SUBMITTED', 'RUNNING_PRO', 'SUSPECTED_STALL'}:
        raise SystemExit(f'heartbeat not appropriate for status {data["status"]}')
    prev = data.get('last_heartbeat_summary')
    summary = args.summary.strip()
    unchanged = bool(prev and prev == summary)
    data['heartbeat_count'] = int(data.get('heartbeat_count', 0)) + 1
    data['last_heartbeat_at'] = now_iso()
    data['last_heartbeat_summary'] = summary
    data['unchanged_heartbeats'] = int(data.get('unchanged_heartbeats', 0)) + 1 if unchanged else 0
    if args.result == 'completed':
        data['status'] = 'COMPLETED'
        data['completed_at'] = now_iso()
    elif args.result == 'auth':
        data['status'] = 'AUTH_REQUIRED'
    elif args.result == 'rate_limited':
        data['status'] = 'RATE_LIMITED'
    elif args.result == 'browser_lost':
        data['status'] = 'BROWSER_LOST'
    elif data['unchanged_heartbeats'] >= args.stall_threshold:
        data['status'] = 'SUSPECTED_STALL'
    else:
        data['status'] = 'RUNNING_PRO'
    data.setdefault('history', []).append({
        'at': now_iso(), 'event': 'heartbeat', 'status': data['status'],
        'result': args.result, 'summary': summary,
    })
    atomic_json(path, data)
    print(json.dumps({
        'job_id': args.job_id,
        'status': data['status'],
        'heartbeat_count': data['heartbeat_count'],
        'unchanged_heartbeats': data['unchanged_heartbeats'],
    }, ensure_ascii=False))
    return 0


def cmd_freeze(args: argparse.Namespace) -> int:
    state = state_path(args.root, args.job_id)
    data = load_json(state)
    source = Path(args.file).resolve()
    if not source.is_file():
        raise SystemExit(f'file not found: {source}')
    content = source.read_bytes()
    digest = hashlib.sha256(content).hexdigest()
    target = job_dir(args.root, args.job_id) / 'response_raw.md'
    if target.exists() and not args.force:
        existing = hashlib.sha256(target.read_bytes()).hexdigest()
        if existing != digest:
            raise SystemExit('response_raw.md already exists with different content; refusing overwrite')
    else:
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_bytes(content)
    data['response_frozen'] = True
    data['response_sha256'] = digest
    old = data['status']
    if old in {'COMPLETED', 'RUNNING_PRO', 'RUNNING_XHIGH', 'SUBMITTED'}:
        data['status'] = 'EXTRACTED'
    data.setdefault('history', []).append({'at': now_iso(), 'event': 'freeze_response', 'sha256': digest, 'status': data['status']})
    atomic_json(state, data)
    print(f'{target}\nsha256={digest}')
    return 0


def cmd_show(args: argparse.Namespace) -> int:
    path = state_path(args.root, args.job_id)
    print(path.read_text(encoding='utf-8'), end='')
    return 0


def cmd_list(args: argparse.Namespace) -> int:
    jobs = project_dir(args.root) / 'jobs'
    rows = []
    if jobs.exists():
        for state in sorted(jobs.glob('*/state.json'), key=lambda x: x.stat().st_mtime, reverse=True):
            try:
                d = load_json(state)
            except Exception:
                continue
            rows.append({
                'job_id': d.get('job_id', state.parent.name),
                'status': d.get('status'),
                'requested_mode': d.get('requested_mode'),
                'topic': d.get('topic'),
                'last_heartbeat_at': d.get('last_heartbeat_at'),
            })
    print(json.dumps(rows, ensure_ascii=False, indent=2))
    return 0


def build_parser() -> argparse.ArgumentParser:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--root', default='.', help='project root containing .gpt-web-review')
    sp = ap.add_subparsers(dest='cmd', required=True)

    s = sp.add_parser('setup')
    s.add_argument('--notes', default='')
    s.add_argument('--force', action='store_true')
    s.set_defaults(func=cmd_setup)

    s = sp.add_parser('new')
    s.add_argument('--topic', required=True)
    s.add_argument('--mode', required=True, choices=['PRO', 'EXTRA_HIGH', 'pro', 'extra_high'])
    s.add_argument('--job-id')
    s.add_argument('--allow-fallback', action='store_true')
    s.add_argument('--force', action='store_true')
    s.set_defaults(func=cmd_new)

    s = sp.add_parser('set')
    s.add_argument('job_id')
    s.add_argument('status')
    s.add_argument('--visible-model')
    s.add_argument('--backend-model')
    s.add_argument('--temporary-chat', choices=['true', 'false'])
    s.add_argument('--chat-url')
    s.add_argument('--note')
    s.add_argument('--force', action='store_true')
    s.set_defaults(func=cmd_set)

    s = sp.add_parser('heartbeat')
    s.add_argument('job_id')
    s.add_argument('--summary', required=True)
    s.add_argument('--result', choices=['running', 'completed', 'auth', 'rate_limited', 'browser_lost'], default='running')
    s.add_argument('--stall-threshold', type=int, default=4)
    s.set_defaults(func=cmd_heartbeat)

    s = sp.add_parser('freeze')
    s.add_argument('job_id')
    s.add_argument('--file', required=True)
    s.add_argument('--force', action='store_true')
    s.set_defaults(func=cmd_freeze)

    s = sp.add_parser('show')
    s.add_argument('job_id')
    s.set_defaults(func=cmd_show)

    s = sp.add_parser('list')
    s.set_defaults(func=cmd_list)
    return ap


def main() -> int:
    args = build_parser().parse_args()
    return int(args.func(args))


if __name__ == '__main__':
    sys.exit(main())
