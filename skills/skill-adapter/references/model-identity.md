# Model identity by host

Reviewed 2026-09-27. Distinguish requested adaptation target, current executing model, and configured default. They can all differ.

Order: explicit user target → trusted host data for the current session/turn → ask once. Do not scan personal transcripts/configs to guess. Only use fields the host actually exposes. Never disclose credentials or full session payloads in reports.

| Host | Reliable evidence when accessible | Limit |
|---|---|---|
| Codex | Explicit model in trusted session context; `/status` output; current session metadata from an integration | `config.toml` is a default, not proof of the current turn. This helper has no automatic Codex transcript scanner. |
| Claude Code | Status-line JSON `model.id`, scoped by `session_id` | Requires a user-configured bridge or supplied payload. Merely installing the skill does not install a status line. |
| Cursor | Hook input `model_id`, otherwise `model`, scoped by `conversation_id` | Auto/routed aliases may hide the actual backend; workspace lifecycle hooks can omit model data. |
| Kimi Code CLI | Current server session status `data.model`, or the active model selected in the session | Kimi CLI and Kimi Code have different release surfaces. Saved `default_model`/aliases may be overridden. Resolve provider alias to actual model when possible. |
| Hermes | Active chat `/model` or `/status`; trusted runtime identity if supplied | Dashboard/config defaults apply to new sessions and can differ from an existing chat; auxiliary models are not the main model. |

The optional helper accepts native Claude status-line, Cursor hook, or Kimi status JSON plus explicit session context; Codex/Hermes integrations can supply a normalized payload. It reads a supplied file only, performs no network calls, and does not install hooks. A local JSON file is only as trustworthy as its producer. The user/integration must supply the current payload and expected session ID; never reuse one global identity file across chats. Reject stale or mismatched captures. Re-capture after a model switch; a TTL alone cannot detect a switch.

Normalized payload example (not a native Codex/Hermes API schema):
```json
{"session_id":"current-session", "model_id":"gpt-6-astra", "captured_at":"2026-09-27T12:00:00+00:00"}
```

Helper usage:
```sh
python3 scripts/model_profile.py --target gpt-6-astra
python3 scripts/model_profile.py --host cursor --payload current-hook.json --session current-conversation
```

Paths above are relative to the installed skill directory. Native live payloads without timestamps require `--live`; this is an assertion by the caller that the payload belongs to this invocation, not automatic proof. Never pass `--live` for a saved stale capture. A Kimi response without a session identifier must be wrapped with the requested session_id and capture time by the caller.

Sources:
- https://learn.chatgpt.com/docs/developer-settings
- https://code.claude.com/docs/en/statusline
- https://prod.cursor.com/docs/hooks
- https://moonshotai.github.io/kimi-code/en/reference/server-api.html
- https://moonshotai.github.io/kimi-code/en/configuration/overrides.html
- https://hermes-agent.nousresearch.com/docs/reference/cli-commands
- https://hermes-agent.nousresearch.com/docs/user-guide/configuring-models
