# Versioned Trip Plans and Budgets

## Choose storage

In LLMWiki-enhanced mode, use LLMWiki for semantic trip versions and Git for
technical history and recovery. A Git commit or branch is not a trip version.
Store the human entry point at `wiki/summary/trips/<trip-id>/overview.md`, shared
items below `items/`, and retained plans below `plans/<variant-id>/<version-id>.md`.
Keep quote, booking, payment, and confirmation evidence immutable in `raw/` and
follow the target Wiki's frontmatter, sources, Wikilinks, observation, and lint
contracts.

In Standalone mode, return the same structure as copyable Markdown and say that
it was not persisted. Never invent a private path or claim future memory.

## Identify trips and versions

Use a readable `trip_id` in the form
`YYYY-primary-region-season-or-purpose`, a readable `variant_id`, and a
sequential `version_id` such as `v001`. Keep the full human-language name in a
separate title. Use only lowercase ASCII letters, numbers, and hyphens in each
identifier. The composite identity is
`<trip-id>/<variant-id>/<version-id>`. Do not put names, birth dates, contact
details, or booking references in identifiers.

A minor date adjustment does not change `trip_id`. Create a new trip identity
only when the main region or purpose changes enough to represent a different
travel decision. Before assigning it, preflight whether the candidate identity already exists.
If multiple trips in the same year would collide, prefer a season or purpose suffix.
If that still collides, append `-2`, then `-3`, using the next
incrementing ASCII number, and repeat the existence preflight until the candidate is unused.
Never overwrite or reuse an existing identity, and do not change the
human-language title merely to resolve a slug collision.

Each variant has one mutable working copy without a `version_id`. Freeze each
coherent comparable plan once as an immutable retained version. Every retained
version contains a complete self-contained itinerary and a complete budget-ledger snapshot.
It is not a budget-only or delta-only record. Deltas are comparison metadata,
never substitutes for either complete snapshot.

Store immutable lineage and its change reason on the new snapshot. `parent_version_id`, `supersedes`, and `common_parent_version_id`
each store the full `<trip-id>/<variant-id>/<version-id>` identity. The first
identifies the parent version, the second identifies any version replaced or
corrected by this successor, and the third identifies the shared origin of a
newly split alternative. The current-selection, cancellation, and finalization records use the same full composite identity.
A bare `version_id` such as `v001` is forbidden as a target
because the same token can exist in more than one variant. After a split, each
variant develops independently.
Do not mutate an old retained snapshot to change its lifecycle disposition.

Derive lifecycle disposition in the overview or a separate mutable index, and
keep at most one selected active baseline per variant. Lifecycle event and selection records target the full composite identity.
For otherwise valid records, apply this deterministic precedence in order:

1. explicit cancellation yields `cancelled`;
2. explicit final selection yields `final`;
3. a successor's `supersedes` yields `superseded`;
4. current selected baseline yields `active`;
5. otherwise yields `draft`.

Thus `draft` is a frozen candidate distinct from the mutable working copy,
`active` is the selected planning baseline, `superseded` was replaced by a
successor, `cancelled` was intentionally abandoned, and `final` is the
selected final trip record. If records violate an invariant, such as multiple
current selections for one variant or contradictory events at the same
precedence, report the conflict and mark the lifecycle `needs-verification` rather than guessing.
The overview or index computes this derived lifecycle disposition without
rewriting retained content.

A material change includes dates, party, primary route, flight, principal
lodging, transport mode, fixed reservations, or a budget change that affects
affordability or the choice between variants. Small editorial changes remain
in the working copy. A current-rate currency refresh is not a plan version.
Correct history with a successor that names the old version in `supersedes`;
record cancellation outside the old snapshot rather than overwriting it. An
explicit privacy deletion or redaction request overrides retention.

## Share evidence without changing history

Give each reusable flight, hotel, transport, ticket, or reservation a readable
shared item ID. Record its provider, service date, traveler scope, original
price, mandatory taxes and fees, inclusions, cancellation and refund terms,
state, evidence revision, and check date.

Updating a shared item never rewrites an old plan snapshot. Each retained plan
references the shared item and evidence revision while preserving the amount
and state used for that decision. A variant that adopts changed facts creates a
successor version.

## Build the budget ledger

Each plan version carries a complete ledger. Every line includes
`budget_item_id`, category, subcategory, description, covered travelers,
quantity, unit, dates, original currency, unit price, mandatory taxes and fees,
discounts, original total, required or optional scope, deadlines, shared item
or source, check date, and assumptions.

Use lifecycle states `estimated`, `quoted`, `booked`, `paid`, `actual`, and
`refunded`. Use fixed categories: flights; lodging; dining; intercity and local transport;
rental vehicle, fuel, tolls, and parking; tickets and experiences;
ski passes, rentals, and lessons; shopping; connectivity and insurance; other costs;
and contingency. Do not double-count bundled meals, tickets, room
packages, or transport. Keep partial-party costs scoped to the correct
travelers.

For an uncertain price, record `low`, `baseline`, and `high` estimates with the
method, evidence, check date, and `needs-verification`. Keep confirmed facts
separate from estimates. Show committed costs with booked and paid subtotals,
required but uncommitted estimates, optional costs, contingency, and the
all-in budget ceiling. The ceiling uses the high case for required and selected
optional items plus contingency and names excluded items.

## Compare currencies and variants

Preserve every original currency and amount. For comparison, recompute all
versions using one current checked rate set and record the exchange-rate source
and check date. Do not mutate retained snapshots or create a version only for
an exchange-rate refresh.

Compare one to three variants or versions by dates, party, route, major items,
category low/baseline/high totals, committed and required costs, optional
costs, contingency, ceiling, current-rate values, delta, risks, and assumptions.
State a concise recommendation without treating it as an external action.

## Update safely

Identify the trip, variant, retained baseline, and working copy. Classify the
change and preserve the immutable baseline. For a material change, apply the
change to a successor working copy, then copy the complete itinerary and complete budget ledger
into the new self-contained snapshot; set its lineage fields and freeze it.
Update shared evidence before the successor adopts those facts, then update the
overview, lifecycle selection, and all plan and shared-item Wikilinks in the
same authorized workflow. Recompute comparisons with one current rate set and
run the target Wiki's required source and lint checks after the write.

If any write or check fails, report the partial state, identify exactly which
pages or links were written, and repair the overview, plan, and shared-item links.
Then rerun source and lint checks, and do not claim success until the stored state is consistent.
Mark missing or conflicting facts `needs-verification` and never infer prices,
refunds, cancellation terms, or confirmation state.

Drafting, comparing, and recommending do not book or cancel anything. Obtain
explicit approval in the current conversation before sending, submitting,
booking, cancelling, or paying.
