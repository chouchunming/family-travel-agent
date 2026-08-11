# Family Travel Agent Generalization Design

Date: 2026-08-11
Status: Approved design, pending implementation

## Goal

Generalize the Japan-centered travel skill into a destination-neutral Family
Travel Agent. Japan becomes the first destination module rather than an
assumption embedded in the core. Existing users of `japan-family-travel` keep
a compatibility entry.

## Chosen approach

Create a new canonical `family-travel-agent` skill and retain
`japan-family-travel` as a small compatibility router.

This avoids breaking existing triggers while giving future destinations a
stable, neutral architecture. The old entry must not become a second
implementation or duplicate the core rules.

## Architecture

### Canonical skill

`skills/family-travel-agent/SKILL.md` is the authoritative workflow. It handles:

- explicit trip scope and traveler-needs discovery;
- family profiles, constraints, accessibility, pace, and trip history;
- evidence quality and current-information checks;
- versioned itineraries, budgets, reservations, activities, dining, and shopping;
- transport handoffs and daily execution plans;
- privacy isolation, approval boundaries, and optional LLMWiki integration;
- selection and loading of destination modules.

The core must use neutral concepts such as `destination navigation identifier`,
`local driving credential`, and `local booking convention`. It must never
silently interpret those concepts as Mapcode, Japanese license translation, or
Japanese reservation etiquette.

### Destination modules

Destination modules live under:

`skills/family-travel-agent/references/destinations/`

Each module owns destination-specific guidance for:

- entry and driving-document requirements;
- local holidays, seasonal closures, and operating calendars;
- transport systems, road rules, tolls, parking, and navigation identifiers;
- taxes, service charges, tipping, payments, and cash expectations;
- cultural, language, dining, hotel, and reservation conventions;
- destination-specific safety and official-source priorities.

`destinations/japan.md` is the first module. It contains Japan-only rules such
as Mapcode and telephone navigation, ETC/tolls, Japanese driving documents,
parking conventions, Japanese addresses, accommodation meal plans, and
reservation-name handling.

A small destination index states which modules exist and prevents unsupported
destinations from inheriting Japan behavior.

### Unsupported destination discovery

When no destination module exists, the core remains usable. It must:

1. identify every destination and border crossing;
2. research current official sources for entry, transport, driving, holidays,
   taxes, payments, safety, reservations, and accessibility;
3. label destination-specific facts with source date and confidence;
4. keep uncertain items as open loops rather than inventing local conventions;
5. propose a reusable destination module only when the findings are durable.

This is the default path for Taiwan, Australia, the United Kingdom, the United
States, and other future destinations until dedicated modules are added.

### Compatibility entry

`skills/japan-family-travel/SKILL.md` remains discoverable for existing
Japan-oriented prompts. It must:

- state that `family-travel-agent` is canonical;
- direct the agent to use the canonical workflow with the Japan module;
- preserve the same privacy, approval, evidence, and LLMWiki boundaries;
- avoid copying the canonical workflow or maintaining a second reference set.

Existing Japan requests therefore continue to work without locking the
architecture to Japan.

## Data and privacy boundary

Every Python travel tool must keep sensitive values in one dedicated, local
private-data file per project. Sensitive values include personal names and
contacts, private addresses, booking/order/ticket identifiers, prices, and
payment data.

The private file must be ignored by Git, use mode `0600` when practical, and
have only a fake tracked example or schema. Private builds fail closed when it
is absent. Public or sanitized builds must not depend on it, so deleting the
file removes the private payload without editing application code.

Public destination data such as Mapcodes, official venue addresses, and
business contact numbers may remain in shareable artifacts. Public outputs
require a source and artifact leak scan before delivery.

## Data flow

1. Capture trip goals, travelers, destinations, dates, constraints, and
   authorization boundaries.
2. Load the neutral core references.
3. Select one destination module per destination; use unsupported-destination
   discovery where none exists.
4. Gather current evidence and separate confirmed facts, recommendations, and
   open loops.
5. Build or update a versioned itinerary and linked reservation/budget state.
6. Produce private execution artifacts or independent sanitized artifacts as
   requested.
7. Write durable knowledge or tasks to a compatible LLMWiki only when
   integration is available and authorized.

## Error handling

- Missing destination module: use discovery mode and disclose the absence.
- Conflicting sources: prefer current primary sources and preserve the conflict
  as an open loop.
- Missing private-data file: private generation stops without using defaults.
- Missing LLMWiki: continue standalone and report that durable fileback was skipped.
- External side effect: obtain explicit approval before booking, purchasing,
  sending, publishing, or changing a remote account.
- Legacy entry without canonical skill: disclose the installation problem
  rather than reproducing stale instructions.

## Documentation and metadata

Update the repository README and OpenAI skill metadata so discovery uses the
neutral Family Travel Agent name while explaining the Japan compatibility
entry.

The repository name may remain `japan-family-travel` for compatibility; the
canonical skill identity changes independently of the repository name.

## Verification design

Static contract tests should prove:

- the canonical skill and destination index exist;
- the core description triggers family travel across destinations;
- Japan-specific tokens are confined to the Japan module or compatibility entry;
- the Japan compatibility entry points to the canonical skill;
- privacy-isolation and external-action approval rules remain present;
- unsupported-destination discovery is explicit;
- tracked examples contain no real traveler or booking data;
- all skill frontmatter and metadata validate.

Existing Japan-focused acceptance scenarios remain useful through the
compatibility entry. Add at least one non-Japan scenario that plans a family
trip without applying Japan-only assumptions.

## Acceptance criteria

The work is complete when:

- `family-travel-agent` is the canonical installed skill;
- Japan is implemented as a destination module;
- `japan-family-travel` remains a non-duplicating compatibility router;
- neutral core references cover the existing cross-destination capabilities;
- unsupported destinations have a safe official-source discovery workflow;
- README, metadata, and contract tests describe the new architecture;
- the LLMWiki task `travel-generalize-family-travel-agent` is marked complete
  only after implementation and verification succeed;
- no commit, push, publish, booking, or other external action occurs without
  separate authorization.
