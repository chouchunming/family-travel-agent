# Family Travel Agent

A reusable Codex skill for family travel across destinations: itineraries,
transport, reservations, experiences, route-aware shopping and dining,
versioned budgets, private traveler preferences, trip history, and local travel
communication.

The neutral core loads destination modules. Japan is the first module and owns
Japan-only holiday, driving, Mapcode, parking, accommodation, reservation,
shopping, dining, and visitor tax guidance.

## Modes

- Standalone: works from itinerary text, documents, confirmations, and URLs.
- LLMWiki-enhanced: optionally uses a detected LLMWiki under its own rules.

The skill never performs an external action without explicit approval.

## Invocation

Use the canonical skill for any destination:

```text
$family-travel-agent Review this multi-country family itinerary.
```

Existing Japan workflows may continue to use the compatibility entry:

```text
$japan-family-travel Review this Japan family itinerary.
```

The compatibility entry routes to `family-travel-agent` plus the Japan module;
it does not maintain a second workflow.

## Install

Link `skills/family-travel-agent` into the Codex skills directory. Optionally
keep `skills/japan-family-travel` linked for backward compatibility. Keep this
repository as the canonical editable source.

## Develop

Run `caffeinate -i -m python3 -m unittest discover -s tests -v` on macOS.

Only anonymous examples belong here. Real trips stay in the user's private
data source. Python travel tools keep sensitive values in one local,
Git-ignored private-data file; public builds must be independent of it.

## Optional LLMWiki integration

No LLMWiki path is configured here. When the current repository or a
user-provided path exposes `wiki_cli.py`, `wiki/`, applicable `AGENTS.md`, and
the installed `llmwiki` skill, the canonical skill may use that repository's
contract. Otherwise it remains standalone and explains the missing capability.

Real-trip acceptance output stays in ignored local storage and is never
committed. Traveler profiles and trip history remain private. With a compatible
LLMWiki, the skill may update them only after explicit confirmation. Without
LLMWiki, it returns a copyable summary and does not silently persist personal data.
