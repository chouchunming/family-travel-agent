# Versioned Trip Plans and Budgets Design

## Goal

Extend `japan-family-travel` with durable, comparable trip-plan variants. Each
retained version must preserve a complete itinerary and detailed budget
snapshot without duplicating shared flight, lodging, ticket, transport, or
reservation evidence.

## Scope

The workflow covers human-readable trip and variant identities, immutable
retained versions, mutable working drafts, shared evidence items, detailed
budget lines, low/baseline/high estimates, lifecycle states, tiered totals,
current-rate currency comparison, and authorized LLMWiki persistence.

It does not automate bookings or payments, add runtime dependencies, migrate
existing private trip pages, or place personal travel data in the public skill
repository.

## Storage architecture

Use LLMWiki for semantic trip versions and Git for technical file history and
recovery. A Git commit or branch is never a trip version identifier because it
may contain unrelated Wiki changes and does not express variant ancestry or
shared booking references.

In LLMWiki-enhanced mode, use this conceptual layout under `wiki/summary/`:

```text
trips/<trip-id>/
├── overview.md
├── items/
│   └── <shared-item-id>.md
└── plans/
    └── <variant-id>/
        └── <version-id>.md
```

The overview is the human entry point and comparison index. Shared item pages
represent reusable flights, hotels, transport, tickets, and reservations.
Plan-version pages are retained itinerary and budget snapshots. Immutable
booking, quote, payment, and confirmation evidence remains in `raw/`; compiled
pages cite exact raw paths and follow the target Wiki's frontmatter, Wikilink,
source, observation, and lint contracts.

## Identity model

Use a readable, stable slug for `trip_id`:

```text
YYYY-primary-region-season-or-purpose
```

For example, an anonymous trip may use
`2027-kansai-winter-family`. Keep the complete human-language name in `title`.
Use lowercase ASCII letters, numbers, and hyphens in identifiers. Never include
traveler names, birth dates, booking references, email addresses, or phone
numbers.

Each alternative has a readable `variant_id`, such as `a-city-first` or
`b-mountain-first`. Each retained snapshot uses a sequential `version_id` such
as `v001`. The composite identity is:

```text
<trip-id>/<variant-id>/<version-id>
```

A minor date adjustment does not change `trip_id`. Create a new trip only when
the main region or purpose changes enough that it is no longer the same travel
decision. Add a season or purpose suffix when multiple trips in one year would
otherwise collide.

## Version lifecycle

Each variant has one mutable working copy. The working copy has no `version_id`
or lifecycle state and is not counted as retained history. Small edits may
accumulate there. Each coherent plan that is worth comparing or selecting is
then frozen exactly once as an immutable retained version containing its parent
version, creation timestamp, change reason, and one of these states:

- `draft`: a frozen candidate proposal that is not the selected plan, distinct
  from the mutable working copy;
- `active`: the currently selected planning baseline;
- `superseded`: replaced by a newer retained version;
- `cancelled`: intentionally abandoned without deleting its history;
- `final`: the version used as the final trip record.

When a material change creates a coherent alternative, retain the unchanged
comparison baseline if needed, apply the change to a successor working copy,
and freeze the changed result as a new version that points to the baseline.
Small edits accumulate in the working copy and enter the next retained snapshot
rather than creating one version per chat message. Creating an alternative
variant records the common parent version, after which each variant develops
independently.

Material changes include the trip date range, traveler composition, primary
route or region, flight, principal lodging, transport mode, fixed reservation,
or a budget change that affects affordability, recommendation, or the choice
between variants. No arbitrary percentage threshold is required. Spelling,
formatting, and explanatory edits may update the working copy without creating
a retained version. Refreshing comparison-only exchange rates does not create
a plan version.

Correct or cancel retained plans by creating a successor and marking the prior
version `superseded` or `cancelled`. Do not overwrite retained content. An
explicit privacy deletion or redaction request overrides retention.

## Shared evidence items

Assign readable stable IDs to reusable items, for example
`flight-city-a-city-b-2027-01-20` or `hotel-city-b-2027-01-22`. Each item records:

- provider, route or venue, service date, and covered travelers;
- official page, sales page, user confirmation, or exact raw evidence;
- original currency, base price, mandatory taxes and fees, and discounts;
- inclusion and exclusion details;
- cancellation, refund, payment, and confirmation state;
- check date and evidence revision.

Updating a shared item never rewrites an old plan snapshot. A plan version
references the item and evidence revision while preserving the original amount
and state used for that decision. A variant that adopts new item facts creates
a successor version.

## Budget ledger

Every plan version contains a complete budget ledger. Each line records:

- `budget_item_id`, category, subcategory, and description;
- covered travelers, quantity, unit, and inclusion dates;
- original currency, unit price, mandatory taxes and fees, discounts, and
  original total;
- lifecycle state: `estimated`, `quoted`, `booked`, `paid`, `actual`, or
  `refunded`;
- required or optional classification;
- payment and cancellation deadlines when applicable;
- shared item or source reference and check date;
- assumptions and `needs-verification` when facts are incomplete.

Use these fixed top-level categories:

- flights;
- lodging;
- dining;
- intercity and local transport;
- rental vehicle, fuel, tolls, and parking;
- tickets and experiences;
- ski passes, rentals, and lessons;
- shopping;
- connectivity and insurance;
- other costs;
- contingency.

Do not double-count an included meal, bundled ticket, room package, or transport
benefit. Preserve item scope so a partial-party activity and the remaining
travelers' expenses can be compared correctly.

## Estimates and totals

For an unconfirmed price, store `low`, `baseline`, and `high` estimates with the
method, evidence, and check date. Never present an unsupported point estimate
as a confirmed price. Replace uncertainty only when a quote, booking, payment,
or actual cost supplies stronger evidence.

For each scenario, show:

1. committed costs, with booked and paid subtotals;
2. required but uncommitted estimates;
3. optional costs;
4. contingency;
5. the all-in budget ceiling.

Keep committed facts separate from estimates. The ceiling uses the high case
for required and selected optional items plus contingency; document any item
excluded from the ceiling.

## Currency comparison

Preserve every original currency and amount. When comparing variants, recompute
all display values in the requested common currency using one current checked
rate set. Record the exchange-rate source and check date. Do not mutate retained
plan snapshots or create a new plan version solely for an exchange-rate refresh.

The comparison view is current-rate analysis, not evidence of the rate used at
booking or payment. A paid card statement or refund retains its actual original
and settlement amounts as evidence.

## Comparison output

Compare one to three named variants or retained versions in a compact table
covering:

- dates, party, route, and major itinerary differences;
- flights, lodging, transport, and fixed ticket differences;
- low/baseline/high totals by category;
- committed, required, optional, contingency, and ceiling totals;
- current-rate common-currency values and rate check date;
- delta from the parent or selected comparison baseline;
- unverified prices, cancellation exposure, and material assumptions;
- a recommendation with a concise reason.

A recommendation does not cancel, replace, submit, or pay for a real booking.

## Update workflow

1. Identify the trip, variant, current retained baseline, and working copy.
2. Classify the requested edit as minor or material.
3. For a material edit, preserve the comparison baseline and freeze the
   coherent changed result as its successor.
4. Update shared item evidence before a successor adopts changed facts.
5. Write the itinerary and full budget snapshot, then update the overview and
   Wikilinks in the same authorized workflow.
6. Recompute comparisons with one current exchange-rate set.
7. Run the target LLMWiki source checks and lint after writes.

In Standalone mode, return the same structure as copyable Markdown and state
that it was not persisted. Never invent a private path or claim future memory.

## Safety and failure handling

- Mark absent or conflicting changing facts `needs-verification`; do not infer
  prices, refunds, cancellation terms, or confirmation state.
- Preserve immutable raw evidence and keep personal data out of the public
  skill, examples, tests, design documents, and plans.
- Require explicit approval in the current conversation before sending,
  submitting, booking, cancelling, or paying.
- A version change never performs an external action or cancels a real booking.
- If an atomic Wiki update cannot complete, report the partial state and repair
  overview, plan, and shared-item links before claiming success.

## Skill structure

Add one focused reference for versioned plans and budgets, and add one concise
row to `SKILL.md` that routes variant, version-history, budget, and trip-cost
comparison requests to it. Keep LLMWiki optional and preserve the explicit-only
activation policy. Add no scripts or runtime dependencies.

## Testing

Extend the packaged reference contract and repository file-shape/privacy tests
before adding production guidance. Tests must require:

- routing to the new reference;
- readable trip, variant, and version identities;
- working-draft versus immutable retained-version behavior;
- parent links, material-change reasons, and lifecycle states;
- shared item references without old-snapshot mutation;
- every fixed budget category and cost lifecycle state;
- low/baseline/high estimates and `needs-verification`;
- tiered totals and all-in ceiling;
- original-currency preservation and current-rate comparison with source and
  check date;
- LLMWiki-only persistence, copyable Standalone output, and explicit approval
  for external actions;
- anonymous examples and absence of private paths or real booking data.

Run the full repository suite, packaged contract, installed-link contract after
local integration, system skill validator, privacy check, and diff check through
`caffeinate -i -m`.

## Non-goals

- No Git branch or commit as a semantic trip version.
- No automatic booking, payment, cancellation, or outbound message.
- No live price scraping, exchange-rate service, or platform API integration.
- No private trip migration in this feature.
- No generated application, database, script, or runtime dependency.
