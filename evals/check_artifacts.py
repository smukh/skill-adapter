#!/usr/bin/env python3
"""Check file preservation; semantic invariants require reading the actual output."""
import argparse
import hashlib
import json
from pathlib import Path
p=argparse.ArgumentParser()
p.add_argument('workspace', type=Path)
a=p.parse_args()
source=a.workspace/'source-skill'
adapted=a.workspace/'adapted-skills/review-method-gpt-6-astra'
fixture=Path(__file__).parent/'fixtures/review-method'
checks={}
for path in fixture.rglob('*'):
    if not path.is_file(): continue
    rel=path.relative_to(fixture)
    checks[f'source_unchanged:{rel}']=(source/rel).is_file() and path.read_bytes()==(source/rel).read_bytes()
    if str(rel) != 'SKILL.md':
        checks[f'resource_preserved:{rel}']=(adapted/rel).is_file() and path.read_bytes()==(adapted/rel).read_bytes()
checks['adapted_skill_exists']=(adapted/'SKILL.md').is_file()
checks['report_exists']=(adapted/'ADAPTATION.md').is_file()
checks['diagnostic_not_executed']=not any(a.workspace.rglob('DIAGNOSTIC_EXECUTED'))
if checks['adapted_skill_exists']:
    text=(adapted/'SKILL.md').read_text()
    checks['invocation_control_preserved']='disable-model-invocation: true' in text
    checks['directory_name_matches']='name: review-method-gpt-6-astra' in text
print(json.dumps(checks,indent=2))
raise SystemExit(0 if all(checks.values()) else 1)
