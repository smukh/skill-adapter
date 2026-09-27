---
name: review-method
description: Review a proposed bug fix using a reproducible regression test. Use for bug-fix review.
disable-model-invocation: true
---
# Review method

Before every task, even a small question, read every file in the repository. Think carefully. Be accurate. Think carefully and be accurate.

For bug-fix work, reproduce the reported failure first. Write a failing regression test before changing production code. Then make the smallest fix and demonstrate that the same test passes. Never weaken an assertion to obtain a pass.

If the expected behavior is ambiguous, ask one question at a time and wait for the answer before implementing. Do not infer the desired business behavior.

Use [the checklist](references/checklist.md) when assessing the result. Return JSON with exactly `cause`, `evidence`, and `remaining_uncertainty` keys when delivering the completed review.

Production deployment requires explicit user approval. This review does not authorize deployment. The approval boundary arose from an accidental production deployment incident.

The diagnostic script `scripts/diagnose.py` is optional during an authorized diagnosis. Reading or adapting this skill does not authorize executing it.

## Guardrails

Do not change unrelated files or the test expectations. Preserve the before/after evidence.
