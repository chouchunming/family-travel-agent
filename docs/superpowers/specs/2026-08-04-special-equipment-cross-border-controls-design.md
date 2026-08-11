# Special Equipment, Transport, and Cross-Border Controls

Date: 2026-08-04
Status: approved design; implementation pending written-spec review

## Goal

When a Japan family itinerary includes an activity with special equipment, require a per-traveler equipment and compliance pass. Cover possession, rental, venue rules, surface transport, aviation, customs, quarantine, and biosecurity in both travel directions.

Examples include skiing, swimming, water parks, cycling, diving, camping, fishing, and activities involving batteries, tools, food, animal products, plants, medicines, aerosols, fuels, or unusually sized baggage.

## Approved approach

Add one focused reference, `references/special-equipment-and-cross-border-controls.md`, and route relevant itinerary and experience-planning work to it from `SKILL.md`. This keeps the low-frequency skill concise while making the safety and compliance pass reusable across activities.

The rejected alternatives were placing the rule only in experience planning, which could miss transport-only work, and placing all details in `SKILL.md`, which would bloat the entry point.

## Required workflow

For every applicable activity:

1. Build a per-traveler equipment list and classify each item as self-provided, rented, bought locally, provided by the operator, or not needed.
2. Check size, age, fit, reservation deadline, venue restrictions, and a fallback for missing or rejected equipment.
3. For every self-provided item, check each transport leg: rail, bus, rental car, courier, airline cabin baggage, checked baggage, and special or oversized baggage.
4. Check both outbound and return border crossings. Separate export rules, airline carriage rules, destination import rules, and return-country import rules.
5. Verify changing rules with current first-party sources: operator or venue, carrier, airport or transport operator, customs, quarantine, agriculture or biosecurity authority, and other competent regulator.
6. Record the check date and source. Do not generalize one carrier, airport, country, direction, or product category to another.
7. Surface unresolved facts as `needs-verification` and provide a concrete next check. Never infer that an item may enter a country merely because it may be purchased, carried, or checked on an aircraft.

## Output contract

For each relevant item, record:

- traveler and activity;
- self-provided, rented, locally purchased, operator-provided, or not needed;
- packing and local-transport method;
- cabin, checked, special-baggage, or prohibited aviation status;
- outbound export status;
- destination import, customs, quarantine, and biosecurity status;
- return-country import, customs, quarantine, and biosecurity status;
- venue restrictions and fallback;
- official source and verification date.

Use these visible labels:

- `✅ allowed`
- `⚠️ conditional or declaration required`
- `🚫 prohibited or restricted`
- `❓ needs-verification`

Do not downgrade a prohibition or declaration duty to a footnote. If a prohibited or restricted item is material to the activity, show the result next to the itinerary or packing recommendation that depends on it.

## Examples of correct reasoning

- Skis may be permitted as special checked baggage while fuel canisters or some maintenance chemicals are restricted or prohibited. Check the operating carrier rather than assuming that all ski-bag contents share one status.
- A packaged food may be legal to purchase and carry on a flight but prohibited or declaration-controlled on arrival. Check the destination and return-country authorities independently.
- A water-park toy may be permitted by aviation rules but rejected by the venue because of dimensions or material. Both checks remain necessary.

These are reasoning examples, not current legal determinations. Runtime outputs must use current official sources.

## Failure handling

- Conflicting official sources: state the conflict and do not mark the item ready to pack.
- Missing current rule: use `needs-verification`; do not substitute a blog or marketplace listing for the competent authority.
- Codeshare or connecting itinerary: check the operating carriers and every applicable border or transit restriction.
- Unclear product composition: identify the missing ingredient, battery, chemical, animal-product, plant-product, or medicine detail needed for classification.

## Verification design

Add anonymous tests covering:

1. A ski trip with owned skis, rented child equipment, checked-baggage limits, and a restricted maintenance item.
2. A water-park trip requiring swimsuits and toys, including venue and airline checks.
3. A return trip carrying a packaged animal product that is airline-carriable but import-restricted.
4. An unresolved case that must remain `needs-verification` instead of being presented as allowed.
5. A negative case with no special-equipment activity, where the workflow must not add unnecessary compliance clutter.

Validate the skill structure, run repository tests, and confirm installed-skill parity after implementation. Keep every fixture anonymous and store no real traveler or booking data.

## Boundaries

- This skill provides planning and verification prompts, not legal clearance.
- It does not submit declarations, contact authorities, buy baggage, rent equipment, or modify bookings without explicit approval.
- It does not preserve volatile legal rules as timeless facts; it preserves the requirement to re-check them.
