# GPT-6 Astra

Revision: 1.0.0. Source-reviewed 2026-09-27. Model-specific guidance; see repository evals for the bounded behavioral receipt.

Source: https://developers.openai.com/blog/rethinking-skills-and-prompts-for-gpt-6-astra (2026-09-11).

Adaptation candidates:
- Replace broad skill triggers with the actual task boundary; retain negative cases where they prevent misrouting.
- Remove duplicated generic coaching; make unrelated preliminary reading conditional on the task. Preserve task-specific prerequisites.
- Express completion and scope clearly so the agent can finish authorized work without artificial interim stopping points.
- Turn redundant generic process narration into outcome/verification criteria when it is not the author's chosen method.
- Keep optional detail behind existing relative references rather than loading every workflow up front.

Do not delete tests, approval gates, incident-specific checks, or deliberate TDD/interview procedures because the model is capable. The source motivates reconsidering generic scaffolding; it does not establish which individual requirement is dispensable. Do not change effort or grant new permissions. Preserve ambiguity as an explicit uncertainty.
