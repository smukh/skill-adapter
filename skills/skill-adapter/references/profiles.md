# Profile index

Revision: 1.0.0. Reviewed 2026-09-27. Read only the selected profile.

| Exact target or documented group | Profile | Evidence before local evaluation |
|---|---|---|
| `gpt-6-astra`, `openai/gpt-6-astra`, user shorthand “Astra 6” | [GPT-6 Astra](profiles/gpt-6-astra.md) | Official model-specific guidance |
| Claude 5 generation: explicit Fable 5/5.1, Mythos 5/5.1, Opus 5/5.5, Sonnet 5 IDs | [Claude 5 generation](profiles/claude-5.md) | Official generation-level guidance; not model-by-model validation |
| `kimi-k3`, `moonshotai/kimi-k3`, explicit “Kimi K3” | [Kimi K3](profiles/kimi-k3.md) | Conservative packaging guidance; no established K3-specific rewrite advantage |
| Other explicit targets, including Claude 4, GPT-6 Sol/Luna, Hermes models, Composer, Gemini, Copilot backends | [Generic](profiles/generic.md) | General preservation/clarity only |

“GPT-6” alone does not identify Astra, Sol, or Luna: clarify. “Claude”, “Kimi”, “Hermes”, “Cursor” and “Auto” do not identify an exact model. Do not borrow another model's behavioral claims. Exact IDs and explicit aliases are recognized by the helper; unlisted snapshots intentionally use generic guidance until a contributor verifies the mapping.

Host portability covers Claude Code, Codex, Kimi Code CLI, Hermes, and Cursor, matching the reference repo. It does not imply knowledge of every model those hosts can run. A profile can be used from any host with the required file tools.
