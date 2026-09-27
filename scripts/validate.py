#!/usr/bin/env python3
"""Dependency-free repository structure and local Markdown link validation."""
from pathlib import Path
import json
import re
root = Path(__file__).resolve().parents[1]
skill = root/'skills/skill-adapter/SKILL.md'
text = skill.read_text()
assert text.startswith('---\n')
front = text.split('---',2)[1]
assert 'name: skill-adapter' in front
assert re.search(r'^description: .+', front, re.M)
assert len(re.search(r'^description: (.+)',front,re.M).group(1)) <= 1024
assert '## Guardrails' in text
for path in root.rglob('*.md'):
    for link in re.findall(r'\]\(([^)]+)\)',path.read_text()):
        if '://' in link or link.startswith('#'): continue
        assert (path.parent/link.split('#')[0]).exists(), (path,link)
for name in ['gpt-6-astra','claude-5','kimi-k3','generic']:
    assert (skill.parent/f'references/profiles/{name}.md').exists()
print('PASS: skill frontmatter, four profile files, local links')
