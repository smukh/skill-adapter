# Compatibility

This package supports Codex, Claude Code, Kimi Code CLI, Hermes, and Cursor through standard directory-form Agent Skills. Host compatibility and model-specific guidance are separate. GPT-6 Astra, Claude 5 generation, and Kimi K3 have profiles; other explicit targets receive generic guidance.

## Evidence boundaries

- Runtime identity parsing: synthetic payload tests for all five documented input routes. These are parser checks, not live integration tests.
- Automatic identity collection: not installed or claimed. Explicit targets work on every host; supplied session payloads require a bridge or user action.
- Claude Code, Cursor, Kimi, Hermes: installation locations and identity sources are documented; live invocation has not been tested in this release.
- Codex and Astra: see [evaluation receipts](evals/RESULTS.md).
- Claude and Kimi profile behavioral quality: untested. Kimi guidance is conservative because model-specific optimization evidence is unavailable.

The whole skill directory must travel together. Unknown model IDs use generic guidance; ambiguous identities require clarification. No skill can guarantee precedence over every other skill or unload prior instructions from a running conversation.

## Skills CLI installation

On 2026-09-27, `skills@1.7.0` discovered exactly one skill from `smukh/skill-adapter`. A project-local installation with `--skill skill-adapter --agent codex --yes` completed in an isolated directory. All 9 package files matched the source byte-for-byte, including profiles, references, and the identity helper. This verifies CLI discovery and copying, not skills.sh leaderboard indexing or live invocation on every host.
