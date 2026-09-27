#!/usr/bin/env python3
"""Run a real isolated Astra adaptation. Uses authenticated Codex; consumes model usage."""
import argparse
import json
from pathlib import Path
import shutil
import subprocess
p=argparse.ArgumentParser()
p.add_argument('--codex',default='codex',help='Codex executable supporting GPT-6 Astra')
p.add_argument('--workspace',type=Path,required=True,help='New output directory outside this repository')
a=p.parse_args()
root=Path(__file__).resolve().parents[1]
w=a.workspace.resolve()
if w.exists(): p.error('Use a new workspace; existing output is never overwritten')
if w == root or root in w.parents: p.error('Keep evaluation output outside the repository')
w.mkdir(parents=True)
shutil.copytree(root/'skills/skill-adapter', w/'.agents/skills/skill-adapter')
shutil.copytree(root/'evals/fixtures/review-method',w/'source-skill')
subprocess.run(['git','init','-q',str(w)],check=True)
prompt='Use the skill-adapter skill at .agents/skills/skill-adapter/SKILL.md to adapt source-skill for GPT-6 Astra. Save a separate complete package under adapted-skills/review-method-gpt-6-astra. Complete its report. Work only inside this isolated workspace. Do not modify source-skill, access the network, or use other installed skills. Finish with created paths and checks performed.'
(w/'prompt.txt').write_text(prompt+'\n')
cmd=[a.codex,'exec','--ignore-user-config','--ephemeral','--model','gpt-6-astra','-c','model_reasoning_effort="medium"','--sandbox','workspace-write','--json','-C',str(w),'-o',str(w/'final.txt'),'-']
(w/'run.json').write_text(json.dumps({'model_requested':'gpt-6-astra','command':cmd,'cli':subprocess.check_output([a.codex,'--version'],text=True).strip()},indent=2))
with (w/'events.jsonl').open('w') as out, (w/'stderr.txt').open('w') as err:
    run=subprocess.run(cmd,input=prompt,text=True,stdout=out,stderr=err)
if run.returncode: raise SystemExit(run.returncode)
subprocess.run(['python3',str(root/'evals/check_artifacts.py'),str(w)],check=True)
print('Review the actual adapted skill for methodology, approval, interaction, and output-contract preservation. Raw transcripts may contain host context; do not publish them unreviewed.')
