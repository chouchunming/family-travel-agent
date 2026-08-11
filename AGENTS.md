# Repository instructions

- Keep the installable skill under `skills/japan-family-travel/`.
- Keep examples and tests anonymous; never add real trip or booking data.
- Do not add runtime dependencies or a `scripts/` directory in version 1.
- Run tests and validation through `caffeinate -i -m` on macOS.
- Keep one tracked `caffeinate -i` assertion alive only during an active orchestration.
- Require explicit user approval for external actions.
- Create focused local commits after verification.
- Never checkpoint a known failing full test suite.
- If no authorized remote exists at handoff, create and verify a durable Git bundle.
- Do not configure a remote, publish, or push without explicit authorization.
