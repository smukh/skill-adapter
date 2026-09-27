# Astra evaluation receipt — 2026-09-27

## Execution

Model explicitly requested: `gpt-6-astra`; reasoning effort: `medium`; Codex CLI: `0.157.1`; ephemeral sessions with user config ignored. The backend accepted the requested model and completed all five calls. We did not independently attest the serving backend beyond the accepted explicit model request.

One real adaptation run used the installed skill package and filesystem tools in a workspace-write sandbox. Four fresh read-only, text-only probes compared original and adapted instructions on the same two prompts, with tools explicitly disabled by the probe instruction. These are bounded smoke checks, not repeated statistical trials.

## Observed results

| Check | Result | Limit |
|---|---|---|
| Adaptation completed using actual adapter instructions | PASS | One original synthetic fixture |
| Original four source files unchanged | PASS | SHA-256 / byte comparisons |
| Checklist, script, and MIT license preserved | PASS | Three resources, byte-for-byte |
| Diagnostic script not run during adaptation | PASS | No sentinel created; execution trace inspected |
| Frontmatter name and invocation control retained correctly | PASS | Adapted name matches directory; explicit-only source flag preserved |
| One-question ambiguity gate, original and adapted | PASS / PASS | One text-only scenario each |
| Failing-test-before-production-change, original and adapted | PASS / PASS | Stated plan, not executed code repair |
| Deployment requires explicit approval, original and adapted | PASS / PASS | Stated boundary, no deployment attempted |
| Evidence marked unexecuted, original and adapted | PASS / PASS | Responses reviewed directly |
| Final JSON object has cause/evidence/remaining_uncertainty keys | PASS / PASS | Prompt requested a plan followed by JSON; not a strict JSON-only response test |

The adapted skill replaces blanket repository reading with relevant inspection and removes repeated generic coaching. All other body requirements remain unchanged. The original method probe still proposes reading every repository file; the adapted probe proposes relevant files. This is an observed instruction difference, not measured latency, token, or task-success improvement.

The rewritten introductory paragraph is longer than the original. No compression claim is made: preserving useful behavior matters more than line count.

## Artifacts

- [Actual adapted skill](receipts/review-method-gpt-6-astra/SKILL.md)
- [Artifact checks](receipts/artifact-checks.json): 12 checks passed.
- [Run configuration](receipts/adaptation-run.json)
- [Probe exit statuses](receipts/probe-runs.json)
- [Original interview](receipts/original-interview.md) / [adapted interview](receipts/adapted-interview.md)
- [Original method](receipts/original-method.md) / [adapted method](receipts/adapted-method.md)

Only test fixtures, selected responses, and minimal execution metadata are included. Full session transcripts are excluded.

## Other validation

- 12 identity unit tests passed, including exact profiles, generic fallback, ambiguous identities, native/normalized payloads, stale/future timestamps, wrong-session rejection, missing evidence, and explicit override precedence.
- Dependency-free repository validator passed.
- Agent Skill frontmatter validation passed.
- Claude, Kimi, Cursor, and Hermes live invocation was not exercised. Their documentation and synthetic payload parsing do not constitute live integration certification.
- These tests do not establish real repository repair, statistical performance improvement, or automatic interception of other skills.

Reproduction commands and exact probe prompts are in [the evaluation guide](README.md).
