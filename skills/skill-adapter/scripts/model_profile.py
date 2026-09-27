#!/usr/bin/env python3
"""Resolve supplied model evidence. Never auto-scan config, transcripts, or credentials."""
import argparse
from datetime import datetime, timezone
import json
from pathlib import Path
import sys

ALIASES = {'astra 6': 'gpt-6-astra', 'gpt-6 astra': 'gpt-6-astra', 'kimi k3': 'kimi-k3'}
CLAUDE = {f'claude-{family}-{version}' for family, versions in [('fable', ['5', '5-1']), ('mythos', ['5', '5-1']), ('opus', ['5', '5-5']), ('sonnet', ['5'])] for version in versions}
AMBIGUOUS = {'', 'auto', 'default', 'latest', 'claude', 'kimi', 'hermes', 'cursor', 'codex', 'gpt-6', 'gpt 6', 'astra'}

def resolve(target):
    if not isinstance(target, str):
        raise ValueError('Model identity must be a string')
    value = target.strip().lower()
    value = ALIASES.get(value, value)
    # Only strip recognized provider namespaces; arbitrary proxy aliases stay generic.
    for provider in ('openai/', 'anthropic/', 'moonshotai/'):
        if value.startswith(provider):
            value = value[len(provider):]
            break
    if value in AMBIGUOUS:
        raise ValueError('Ambiguous model identity; request an exact target model')
    if value == 'gpt-6-astra':
        profile, evidence = 'gpt-6-astra', 'official-model-guidance'
    elif value in CLAUDE:
        profile, evidence = 'claude-5', 'experimental-generation-guidance'
    elif value == 'kimi-k3':
        profile, evidence = 'kimi-k3', 'experimental-conservative'
    else:
        profile, evidence = 'generic', 'no-model-specific-guidance'
    return {'target': target, 'normalized_model': value, 'profile': profile,
            'profile_revision': '1.0.0', 'evidence': evidence,
            'profile_path': str(Path(__file__).resolve().parents[1] / 'references' / 'profiles' / f'{profile}.md')}

def from_payload(host, payload, session, live=False, now=None):
    if not isinstance(payload, dict):
        raise ValueError('Payload must be an object')
    key = 'conversation_id' if host == 'cursor' else 'session_id'
    if not session or payload.get(key) != session:
        raise ValueError('Missing or mismatched current session identity')
    timestamp = payload.get('captured_at')
    if timestamp is None and not live:
        raise ValueError('Capture timestamp required; --live is only for a fresh native payload')
    if timestamp is not None:
        stamp = datetime.fromisoformat(timestamp.replace('Z', '+00:00'))
        if stamp.tzinfo is None:
            raise ValueError('Capture timestamp must include a timezone')
        age = ((now or datetime.now(timezone.utc)) - stamp).total_seconds()
        if age < -5 or age > 60:
            raise ValueError('Stale or future model identity; capture the current turn again')
    if host == 'claude-code':
        model = payload.get('model', {})
        model = model.get('id') if isinstance(model, dict) else None
    elif host == 'cursor':
        model = payload.get('model_id') or payload.get('model')
    elif host == 'kimi':
        data = payload.get('data', {})
        model = data.get('model') if isinstance(data, dict) else None
    else:
        model = payload.get('model_id')  # Explicit normalized bridge schema.
    if not model:
        raise ValueError('No model identity supplied by this host payload')
    result = resolve(model)
    result.update(identity_source=f'{host}-supplied-session-payload', session_id=session)
    return result

def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--target')
    parser.add_argument('--host', choices=['codex', 'claude-code', 'cursor', 'kimi', 'hermes'])
    parser.add_argument('--payload', type=Path)
    parser.add_argument('--session')
    parser.add_argument('--live', action='store_true')
    args = parser.parse_args()
    try:
        if args.target is not None:
            result = resolve(args.target)
            result['identity_source'] = 'explicit-target'
        elif args.host and args.payload and args.session:
            result = from_payload(args.host, json.loads(args.payload.read_text()), args.session, args.live)
        else:
            raise ValueError('Supply --target, or --host --payload --session with current evidence')
        print(json.dumps(result, indent=2))
        return 0
    except (ValueError, OSError, TypeError) as error:
        print(json.dumps({'status': 'needs-model-evidence', 'error': str(error)}))
        return 2

if __name__ == '__main__':
    sys.exit(main())
