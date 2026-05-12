# Agent Guidance

- Do not add required runtime dependencies without explicit approval.
- Keep all scripts Python stdlib-only unless explicitly approved.
- Do not include real Home Assistant tokens, URLs, secrets, or personal entity names.
- Prefer docs and templates over live Home Assistant mutation.
- Do not connect to a live Home Assistant instance from this repository.
- Any change to high-privilege plugins must update `docs/security-model.md`.
- Run validation scripts with `uv run python` before final response.
- Keep upstream integrations as references/templates rather than vendored code.
- If plugin schemas are ambiguous, document the ambiguity in `docs/implementation-notes.md`.
