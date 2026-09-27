# Bounded Astra evaluation

Use Codex CLI with an explicit `--model gpt-6-astra`, in an isolated directory. The fixture is original MIT text written for this project. It combines procedural requirements, interaction gates, an exact output contract, duplicate coaching, a relative checklist, and a script that must not execute during adaptation.

1. Copy the adapter package and fixtures into a fresh workspace.
2. Ask the target model to adapt the fixture, preserving methodology and resources.
3. Inspect the actual adapted SKILL.md and report, source hashes, resources, and sentinel.
4. Run original and adapted instructions on the same two behavioral probes in fresh calls: an interview gate and a TDD ordering question.
5. Record exact model request, CLI version, commands, outcomes, and limitations.

This is an adaptation correctness smoke test, not a statistical benchmark or proof of performance improvement. The executing model's output is reviewed against observable invariants. No tests are run against Claude or Kimi. See [results](RESULTS.md).

## Reproduce adaptation

Use Codex CLI 0.157.1 or a release supporting GPT-6 Astra. CLI 0.143.0 was rejected by the backend.

```sh
python3 evals/run_astra.py --workspace /tmp/skill-adapter-astra-new
# Or supply a workspace-local executable:
python3 evals/run_astra.py --codex /path/to/codex --workspace /tmp/skill-adapter-astra-another
```

This consumes authenticated Codex model usage. It does not install or upgrade the CLI. Existing output directories are refused.

Reproduce the text-only preservation comparison in four fresh sessions:
```sh
python3 evals/probe_astra.py --workspace /tmp/skill-adapter-probes-new --adapted /tmp/skill-adapter-astra-new/adapted-skills/review-method-gpt-6-astra/SKILL.md
```
The runner uses at most two concurrent calls and writes each response separately. Review the actual responses; it does not use keyword matching as a proxy for behavioral correctness. The no-tools probe condition intentionally isolates instruction following and does not test repository exploration or real bug fixing.
