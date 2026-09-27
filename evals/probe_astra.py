import concurrent.futures
import json
from pathlib import Path
import subprocess
import argparse
parser=argparse.ArgumentParser(description='Run four text-only Astra probes; consumes authenticated Codex usage.')
parser.add_argument('--workspace',type=Path,required=True)
parser.add_argument('--adapted',type=Path,required=True,help='Adapted SKILL.md from an actual adaptation run')
parser.add_argument('--codex',default='codex')
args=parser.parse_args()
cli=args.codex
w=args.workspace.resolve()
if w.exists(): parser.error('Use a new workspace')
w.mkdir(parents=True)
repo=Path(__file__).resolve().parents[1]
original=(repo/'evals/fixtures/review-method/SKILL.md').read_text()
adapted=args.adapted.read_text()
def run(case):
 variant,probe=case
 d=w/f'{variant}-{probe}';d.mkdir(exist_ok=True)
 skill=original if variant=='original' else adapted
 task=(repo/f'evals/probes/{probe}.txt').read_text()
 prompt='This is an isolated text-only behavioral probe. Use no tools. Apply this skill to the task below. Do not adapt or critique the skill.\n\n<skill>\n'+skill+'\n</skill>\n\n'+task
 (d/'prompt.txt').write_text(prompt)
 cmd=[str(cli),'exec','--ignore-user-config','--ephemeral','--skip-git-repo-check','--model','gpt-6-astra','-c','model_reasoning_effort="medium"','--sandbox','read-only','--json','-C',str(d),'-o',str(d/'response.txt'),'-']
 with (d/'events.jsonl').open('w') as out,(d/'stderr.txt').open('w') as err:
  result=subprocess.run(cmd,input=prompt,text=True,stdout=out,stderr=err)
 return {'variant':variant,'probe':probe,'exit_code':result.returncode}
with concurrent.futures.ThreadPoolExecutor(max_workers=2) as pool:
 results=list(pool.map(run,[(v,p) for v in ['original','adapted'] for p in ['interview','method']]))
(w/'runs.json').write_text(json.dumps(results,indent=2))
print(json.dumps(results))
