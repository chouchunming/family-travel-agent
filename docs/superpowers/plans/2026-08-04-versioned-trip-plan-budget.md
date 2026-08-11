# Versioned Trip Plans and Budgets Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Add a tested, reusable workflow that preserves named trip-plan variants, immutable itinerary and budget snapshots, shared evidence items, and current-rate cost comparisons.

**Architecture:** Keep `SKILL.md` as a concise router and place semantic versioning, LLMWiki storage, shared-item, budget-ledger, estimate, total, and comparison rules in one new `references/versioned-trip-plans-and-budgets.md`. Extend packaged and repository contracts before adding the reference, then verify the feature in an isolated worktree without changing the installed global symlink.

**Tech Stack:** Markdown skill package, Python `unittest`, Codex skill validator, Git.

## Global Constraints

- Preserve explicit-only invocation and optional LLMWiki integration.
- Use LLMWiki for semantic trip versions and Git only for technical history and recovery.
- Keep every retained plan version immutable; an explicit privacy deletion or redaction request overrides retention.
- Preserve original currencies; recompute comparison values with one current checked rate set and record its source and check date.
- Do not add scripts, runtime dependencies, private paths, credentials, real traveler data, booking automation, payment automation, or live migration of private Wiki pages.
- Run every test and validation command through `caffeinate -i -m` on macOS.
- Maintain one tracked orchestration-scoped `caffeinate -i` assertion only while execution is active.
- Work on branch `feat/versioned-trip-budgets` in an ignored linked worktree under `.worktrees/`.
- Never checkpoint a known failing full suite. Commit only after RED becomes GREEN and the full suite passes.
- The repository has no authorized remote. Create and verify a durable Git bundle before any execution handoff.
- Do not change the global installed skill symlink from the feature worktree. Run its opt-in contract only after local integration to `main`.

---

### Task 0: Establish the isolated green baseline

**Files:**
- Verify: repository state and `.worktrees/` ignore rule
- Test: `tests/test_skill.py`

**Interfaces:**
- Consumes: approved design commit and this implementation plan on clean `main`.
- Produces: linked worktree `.worktrees/versioned-trip-budgets` on branch `feat/versioned-trip-budgets` with a green baseline.

- [ ] **Step 1: Start and track the execution power assertion**

Run from the canonical repository in a PTY-backed session:

```bash
caffeinate -i
```

Expected: the process remains alive for the active orchestration. Record its
session identifier and stop it before pausing or handing control back.

- [ ] **Step 2: Verify canonical state and worktree isolation prerequisites**

Run:

```bash
git branch --show-current
git status --short
git rev-parse --git-dir
git rev-parse --git-common-dir
git rev-parse --show-superproject-working-tree
git check-ignore -q .worktrees
```

Expected: branch `main`, clean status, no superproject output, Git dir and
common dir identify the canonical checkout, and `.worktrees` is ignored.

- [ ] **Step 3: Create the feature worktree**

Run from the canonical repository:

```bash
git worktree add .worktrees/versioned-trip-budgets -b feat/versioned-trip-budgets
```

Expected: Git creates the named branch and linked worktree from current `main`.

- [ ] **Step 4: Verify linked-worktree state**

Run from `.worktrees/versioned-trip-budgets`:

```bash
git rev-parse --git-dir
git rev-parse --git-common-dir
git rev-parse --show-superproject-working-tree
git branch --show-current
git status --short
```

Expected: Git dir differs from common dir, there is no superproject, branch is
`feat/versioned-trip-budgets`, and status is clean.

- [ ] **Step 5: Run the clean baseline**

Run:

```bash
caffeinate -i -m python3 -m unittest discover -s tests -v
```

Expected: 10 tests pass with the opt-in installed-link test skipped. Stop and
investigate if any baseline test fails.

---

### Task 1: Add the versioned-plan contract and minimal workflow

**Files:**
- Modify: `skills/japan-family-travel/tests/test_reference_contract.py`
- Modify: `tests/test_skill.py`
- Create: `skills/japan-family-travel/references/versioned-trip-plans-and-budgets.md`
- Modify: `skills/japan-family-travel/SKILL.md`
- Test: `skills/japan-family-travel/tests/test_reference_contract.py`
- Test: `tests/test_skill.py`

**Interfaces:**
- Consumes: the approved identity, lifecycle, shared-item, budget, currency, persistence, and external-action contracts.
- Produces: routed reference `references/versioned-trip-plans-and-budgets.md` with anonymous, dependency-free instructions.

- [ ] **Step 1: Write failing packaged and file-shape contracts**

Add the new filename to `REFERENCES` in
`skills/japan-family-travel/tests/test_reference_contract.py`:

```python
REFERENCES = (
    "experience-planning.md",
    "itinerary-workflow.md",
    "mapcode-navigation.md",
    "reservation-workflow.md",
    "evidence-and-needs-discovery.md",
    "shopping-and-dining.md",
    "traveler-profile-and-history.md",
    "versioned-trip-plans-and-budgets.md",
)
```

Add these methods to `ReferenceContractTests`:

```python
def test_versioned_plans_use_readable_immutable_lineage(self):
    reference = (
        SKILL_ROOT
        / "references"
        / "versioned-trip-plans-and-budgets.md"
    )
    self.assertTrue(reference.is_file(), reference)
    text = reference.read_text(encoding="utf-8")
    for phrase in (
        "YYYY-primary-region-season-or-purpose",
        "`trip_id`",
        "`variant_id`",
        "`version_id`",
        "mutable working copy",
        "immutable retained version",
        "parent version",
        "change reason",
        "material change",
        "privacy deletion or redaction",
    ):
        self.assertIn(phrase, text)
    for state in ("draft", "active", "superseded", "cancelled", "final"):
        self.assertIn(f"`{state}`", text)

def test_versioned_budgets_preserve_items_categories_and_ranges(self):
    reference = (
        SKILL_ROOT
        / "references"
        / "versioned-trip-plans-and-budgets.md"
    )
    self.assertTrue(reference.is_file(), reference)
    text = reference.read_text(encoding="utf-8")
    for phrase in (
        "shared item",
        "evidence revision",
        "never rewrites an old plan snapshot",
        "`budget_item_id`",
        "flights",
        "lodging",
        "dining",
        "intercity and local transport",
        "rental vehicle, fuel, tolls, and parking",
        "tickets and experiences",
        "ski passes, rentals, and lessons",
        "shopping",
        "connectivity and insurance",
        "other costs",
        "contingency",
        "`low`",
        "`baseline`",
        "`high`",
        "committed costs",
        "required but uncommitted estimates",
        "optional costs",
        "all-in budget ceiling",
    ):
        self.assertIn(phrase, text)
    for state in ("estimated", "quoted", "booked", "paid", "actual", "refunded"):
        self.assertIn(f"`{state}`", text)

def test_versioned_plan_storage_currency_and_action_boundaries(self):
    reference = (
        SKILL_ROOT
        / "references"
        / "versioned-trip-plans-and-budgets.md"
    )
    self.assertTrue(reference.is_file(), reference)
    text = reference.read_text(encoding="utf-8")
    for phrase in (
        "LLMWiki-enhanced mode",
        "Standalone mode",
        "copyable Markdown",
        "A Git commit or branch is not a trip version",
        "original currency",
        "current checked rate set",
        "exchange-rate source",
        "check date",
        "one to three",
        "needs-verification",
        "explicit approval",
    ):
        self.assertIn(phrase, text)
```

Add the reference to the expected package shape in
`test_version_one_file_shape`:

```python
"references/versioned-trip-plans-and-budgets.md",
```

Add the public path to the repository `expected` set in
`test_every_public_candidate_is_expected_text_without_private_data`:

```python
"skills/japan-family-travel/references/versioned-trip-plans-and-budgets.md",
```

- [ ] **Step 2: Run focused tests and verify RED**

Run:

```bash
caffeinate -i -m python3 skills/japan-family-travel/tests/test_reference_contract.py -v
caffeinate -i -m python3 -m unittest tests/test_skill.py -v
```

Expected: assertion failures because the new reference does not exist and the
router does not link it. The repository test also reports the expected but
missing file. There must be no `FileNotFoundError`, syntax error, or unrelated
failure. Do not commit this known failing state.

- [ ] **Step 3: Create the minimal versioned-plan reference**

Create
`skills/japan-family-travel/references/versioned-trip-plans-and-budgets.md`
with exactly this initial content:

```markdown
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
separate title. Do not put names, birth dates, contact details, or booking
references in identifiers.

Each variant has one mutable working copy without a `version_id`. Freeze each
coherent comparable plan once as an immutable retained version with a parent
version, creation timestamp, and change reason. Use states `draft`, `active`,
`superseded`, `cancelled`, and `final`. A frozen `draft` is distinct from the
mutable working copy.

A material change includes dates, party, primary route, flight, principal
lodging, transport mode, fixed reservations, or a budget change that affects
affordability or the choice between variants. Small editorial changes remain
in the working copy. A current-rate currency refresh is not a plan version.
Correct or cancel history with a successor rather than overwriting it. An
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
`refunded`. Use fixed categories: flights; lodging; dining; intercity and local
transport; rental vehicle, fuel, tolls, and parking; tickets and experiences;
ski passes, rentals, and lessons; shopping; connectivity and insurance; other
costs; and contingency. Do not double-count bundled meals, tickets, room
packages, or transport. Keep partial-party costs scoped to the correct
travelers.

For an uncertain price, record `low`, `baseline`, and `high` estimates with the
method, evidence, check date, and `needs-verification`. Keep confirmed facts
separate from estimates. Show committed costs with booked and paid subtotals,
required but uncommitted estimates, optional costs, contingency, and the all-in
budget ceiling. The ceiling uses the high case for required and selected
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
change, preserve the baseline, update shared evidence, freeze a coherent
successor, and update overview and Wikilinks together. Run the target Wiki's
required source and lint checks after an authorized write. Mark missing or
conflicting facts `needs-verification` and never infer prices, refunds,
cancellation terms, or confirmation state.

Drafting, comparing, and recommending do not book or cancel anything. Obtain
explicit approval in the current conversation before sending, submitting,
booking, cancelling, or paying.
```

- [ ] **Step 4: Route version and budget requests from the main skill**

Add this row to `skills/japan-family-travel/SKILL.md` under `Route by need`:

```markdown
| Trip variants, version history, budget detail, cost comparison | [versioned plans and budgets](references/versioned-trip-plans-and-budgets.md) |
```

Do not duplicate the reference's data model in `SKILL.md`.

- [ ] **Step 5: Run focused tests and verify GREEN**

Run:

```bash
caffeinate -i -m python3 skills/japan-family-travel/tests/test_reference_contract.py -v
caffeinate -i -m python3 -m unittest tests/test_skill.py -v
```

Expected: both commands exit 0. The packaged suite runs 16 tests after adding
three reference contracts; the repository suite runs 10 tests with one opt-in
installed-link skip.

- [ ] **Step 6: Run the full suite before checkpointing**

Run:

```bash
caffeinate -i -m python3 -m unittest discover -s tests -v
caffeinate -i -m python3 "$HOME/.codex/skills/.system/skill-creator/scripts/quick_validate.py" skills/japan-family-travel
caffeinate -i -m git diff --check
```

Expected: 10 repository tests pass with one opt-in skip, the validator reports
`Skill is valid!`, and the diff check prints no errors.

- [ ] **Step 7: Review scope and privacy**

Run:

```bash
git status --short --branch
git diff --stat
git diff -- skills/japan-family-travel/SKILL.md skills/japan-family-travel/references/versioned-trip-plans-and-budgets.md skills/japan-family-travel/tests/test_reference_contract.py tests/test_skill.py
```

Expected: only the main router, new anonymous reference, two contract files,
and no unrelated or private data changes. Confirm no booking IDs, email
addresses, phone numbers, credentials, personal absolute paths, runtime
dependencies, scripts, or external-action automation entered the package.

- [ ] **Step 8: Commit the independently reviewable feature**

Run:

```bash
git add tests/test_skill.py skills/japan-family-travel/tests/test_reference_contract.py skills/japan-family-travel/SKILL.md skills/japan-family-travel/references/versioned-trip-plans-and-budgets.md
git commit -m "feat: add versioned trip budgets"
```

Expected: one focused feature commit and clean worktree status.

---

### Task 2: Verify the committed branch and create a durable checkpoint

**Files:**
- Verify: complete `feat/versioned-trip-budgets` branch
- Create outside repository: durable bundle named with the feature commit's short SHA

**Interfaces:**
- Consumes: the committed routed reference and contracts from Task 1.
- Produces: fresh verification evidence and a complete recoverable Git bundle containing `feat/versioned-trip-budgets`.

- [ ] **Step 1: Run fresh committed-state verification**

Run from the feature worktree:

```bash
caffeinate -i -m python3 -m unittest discover -s tests -v
caffeinate -i -m python3 skills/japan-family-travel/tests/test_reference_contract.py -v
caffeinate -i -m python3 "$HOME/.codex/skills/.system/skill-creator/scripts/quick_validate.py" skills/japan-family-travel
caffeinate -i -m git show --check --oneline --summary HEAD
```

Expected: all tests pass, the validator succeeds, and the committed diff has no
whitespace errors. Keep the installed-link test skipped here because the global
symlink intentionally resolves to canonical `main`, not the feature worktree.

- [ ] **Step 2: Verify durable-object and branch state**

Run:

```bash
git rev-parse --path-format=absolute --git-common-dir
git branch --show-current
git status --short --branch
git log -1 --oneline --decorate
```

Expected: the common Git object database is in the durable canonical clone,
branch is `feat/versioned-trip-budgets`, status is clean, and `HEAD` is the
feature commit.

- [ ] **Step 3: Create and verify the durable branch bundle**

Resolve the short SHA and bundle path, then create the bundle in the existing
durable checkpoint directory:

```bash
JFT_COMMON_DIR="$(git rev-parse --path-format=absolute --git-common-dir)"
JFT_CANONICAL_REPO="$(dirname "$JFT_COMMON_DIR")"
JFT_CHECKPOINT_DIR="$(dirname "$JFT_CANONICAL_REPO")/japan-family-travel-checkpoints"
JFT_FEATURE_SHA="$(git rev-parse --short HEAD)"
JFT_BUNDLE="$JFT_CHECKPOINT_DIR/japan-family-travel-versioned-trip-budgets-${JFT_FEATURE_SHA}.bundle"
mkdir -p "$JFT_CHECKPOINT_DIR"
test ! -e "$JFT_BUNDLE"
caffeinate -i -m git bundle create "$JFT_BUNDLE" feat/versioned-trip-budgets
caffeinate -i -m git bundle verify "$JFT_BUNDLE"
caffeinate -i -m git bundle list-heads "$JFT_BUNDLE"
```

Expected: the collision preflight succeeds, verification reports complete
history, and `list-heads` reports `refs/heads/feat/versioned-trip-budgets` at
`HEAD`.

- [ ] **Step 4: Stop the orchestration power assertion before handoff**

Send interrupt to the tracked `caffeinate -i` session and verify only unrelated
assertions, if any, remain. Do not kill another workflow's process.

---

### Task 3: Finish the development branch according to the user's choice

**Files:**
- Verify: feature branch and canonical `main`
- Preserve or remove: `.worktrees/versioned-trip-budgets`

**Interfaces:**
- Consumes: verified feature commit and complete durable bundle from Task 2.
- Produces: one explicitly chosen merge, PR, preserved branch, or confirmed discard outcome.

- [ ] **Step 1: Offer the four branch outcomes**

Present exactly:

```text
Implementation complete. What would you like to do?

1. Merge back to main locally
2. Push and create a Pull Request
3. Keep the branch as-is (I'll handle it later)
4. Discard this work

Which option?
```

No remote exists, so option 2 requires separate explicit authorization to
configure or use a remote. Option 4 requires the user to type `discard` before
deleting work.

- [ ] **Step 2: For local merge, fast-forward and verify canonical main**

If the user selects option 1, start a new tracked orchestration-scoped
`caffeinate -i`, verify both worktrees are clean, and run from the canonical
repository:

```bash
caffeinate -i -m git merge --ff-only feat/versioned-trip-budgets
caffeinate -i -m python3 -m unittest discover -s tests -v
JFT_REQUIRE_INSTALLED_LINK=1 JFT_INSTALLED_LINK="$HOME/.codex/skills/japan-family-travel" caffeinate -i -m python3 -m unittest discover -s tests -v
caffeinate -i -m python3 skills/japan-family-travel/tests/test_reference_contract.py -v
caffeinate -i -m python3 "$HOME/.codex/skills/.system/skill-creator/scripts/quick_validate.py" skills/japan-family-travel
```

Expected: fast-forward merge succeeds; repository, installed-link, packaged,
and validator checks all pass with no installed-link skip.

- [ ] **Step 3: For local merge, verify reachability and clean up**

Before cleanup, run:

```bash
git merge-base --is-ancestor feat/versioned-trip-budgets main
JFT_COMMON_DIR="$(git rev-parse --path-format=absolute --git-common-dir)"
JFT_CANONICAL_REPO="$(dirname "$JFT_COMMON_DIR")"
JFT_CHECKPOINT_DIR="$(dirname "$JFT_CANONICAL_REPO")/japan-family-travel-checkpoints"
JFT_FEATURE_SHA="$(git rev-parse --short feat/versioned-trip-budgets)"
JFT_BUNDLE="$JFT_CHECKPOINT_DIR/japan-family-travel-versioned-trip-budgets-${JFT_FEATURE_SHA}.bundle"
caffeinate -i -m git bundle verify "$JFT_BUNDLE"
git -C .worktrees/versioned-trip-budgets status --short --branch
```

Expected: ancestor check exits 0, bundle remains complete, and feature worktree
is clean. Then run from the canonical repository:

```bash
JFT_WORKTREE="$JFT_CANONICAL_REPO/.worktrees/versioned-trip-budgets"
caffeinate -i -m git worktree remove "$JFT_WORKTREE"
caffeinate -i -m git branch -d feat/versioned-trip-budgets
git status --short --branch
git log -1 --oneline --decorate
```

Expected: only the canonical `main` worktree remains, feature branch is deleted,
main is clean, and `HEAD` is the verified feature commit. Stop the tracked
power assertion before final handoff.
