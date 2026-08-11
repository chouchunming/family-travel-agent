# Experience Planning Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Add a tested, reusable workflow for discovering and comparing family-suitable Japan experiences across official operators, Agoda, KKday, and Klook.

**Architecture:** Keep `SKILL.md` as a concise router and place detailed activity discovery, verification, family-fit, channel-comparison, and booking-boundary guidance in one new `references/experience-planning.md` file. Extend both packaged and repository-level contract tests before adding production guidance.

**Tech Stack:** Markdown skill package, Python `unittest`, Codex skill validator, Git.

## Global Constraints

- Preserve explicit-only invocation and optional LLMWiki integration.
- Do not add scripts, runtime dependencies, private paths, credentials, affiliate behavior, or real traveler data.
- Do not automate booking, payment, cancellation, or outbound messages.
- Run every test or validation command through `caffeinate -i -m` on macOS.
- Keep the canonical Git object database on durable storage and create a durable verified bundle because the repository intentionally has no remote.
- Keep public documentation free of personal absolute paths so the repository privacy contract continues to pass.
- Execute implementation on the named branch `feat/experience-planning` in an isolated worktree; do not implement on `main`.
- Verify a clean full-suite baseline before introducing the feature's failing tests.

---

### Task 0: Verify the clean implementation baseline

**Files:**
- Verify: repository tests and current branch state

**Interfaces:**
- Consumes: the approved design, plan, and their already-verified public-file contract.
- Produces: evidence that feature RED failures will be attributable only to the new feature.

- [ ] **Step 1: Verify worktree and branch isolation**

Run:

```bash
git rev-parse --git-dir
git rev-parse --git-common-dir
git rev-parse --show-superproject-working-tree
git branch --show-current
git status --short
```

Expected: a linked worktree on `feat/experience-planning`, no superproject, and
a clean status. Stop if execution is on `main`, detached, or dirty.

- [ ] **Step 2: Verify the full baseline is green**

Run:

```bash
caffeinate -i -m python3 -m unittest discover -s tests -v
```

Expected: 10 tests run, all pass, with one opt-in installed-link test skipped.
Stop and investigate before feature work if any test fails.

---

### Task 1: Add failing reference and package-shape contracts

**Files:**
- Modify: `skills/japan-family-travel/tests/test_reference_contract.py`
- Modify: `tests/test_skill.py`
- Test: `skills/japan-family-travel/tests/test_reference_contract.py`
- Test: `tests/test_skill.py`

**Interfaces:**
- Consumes: the approved experience-planning design.
- Produces: a failing contract that names the new reference file and its required behavior.

- [ ] **Step 1: Add the new reference to the packaged router contract**

Add `"experience-planning.md"` to `REFERENCES` in
`skills/japan-family-travel/tests/test_reference_contract.py`.

- [ ] **Step 2: Add the experience-planning behavior contract**

Add this test to `ReferenceContractTests`:

```python
def test_experience_planning_compares_channels_and_family_fit(self):
    reference = SKILL_ROOT / "references" / "experience-planning.md"
    self.assertTrue(reference.is_file(), reference)
    text = reference.read_text(encoding="utf-8")
    for phrase in (
        "Agoda",
        "KKday",
        "Klook",
        "official operator",
        "one to three",
        "family fit",
        "route efficiency",
        "total party price",
        "language",
        "cancellation",
        "weather",
        "unresolved conflict",
        "mandatory taxes and fees",
        "exchange-rate source",
        "check date",
        "needs-verification",
        "request receipt is not confirmation",
        "explicit approval",
    ):
        self.assertIn(phrase, text)
```

- [ ] **Step 3: Extend repository file-shape expectations**

Add `references/experience-planning.md` to the `relative` expected set in
`test_version_one_file_shape` and add the new reference to the repository
`expected` set in
`test_every_public_candidate_is_expected_text_without_private_data`:

```python
"skills/japan-family-travel/references/experience-planning.md",
```

- [ ] **Step 4: Run the focused tests and verify RED**

Run:

```bash
caffeinate -i -m python3 skills/japan-family-travel/tests/test_reference_contract.py -v
caffeinate -i -m python3 -m unittest tests/test_skill.py -v
```

Expected: assertion failures because `references/experience-planning.md` does
not exist, the router does not link it, and the package does not yet contain
it. There must be no `FileNotFoundError`, syntax error, or unrelated failure.

---

### Task 2: Add the minimal experience workflow and router entry

**Files:**
- Create: `skills/japan-family-travel/references/experience-planning.md`
- Modify: `skills/japan-family-travel/SKILL.md`
- Test: `skills/japan-family-travel/tests/test_reference_contract.py`
- Test: `tests/test_skill.py`

**Interfaces:**
- Consumes: the failing contracts from Task 1 and reservation states in `references/reservation-workflow.md`.
- Produces: the routed `experience-planning.md` reference used for activities, tours, tickets, workshops, factory visits, and bookable experiences.

- [ ] **Step 1: Create the minimal reference**

Create `references/experience-planning.md` with these sections and rules:

```markdown
# Experience Planning

## Discover and verify

Search the official operator and relevant Agoda, KKday, or Klook listings.
No candidate must appear on every channel. Use an available official operator
source to cross-check the experience, operating date, eligibility, access, and
core restrictions. Use each sales page for its own availability, total party
price, inclusions, payment, cancellation, refund, language, transport, weather,
and platform-added benefits. When sources conflict, use the official operator
for operating dates, eligibility, access, safety, and core restrictions, and
use each seller for that seller's commercial terms. If an unresolved conflict
affects date, eligibility, or safety, label it and do not present the candidate
as ready to book. Record the check date. Mark missing changing facts as
`needs-verification`; never infer them.

## Check family fit and route

Compare age, height, health, language, duration, meeting point, transport,
included and excluded items, meals, rest, fixed reservations, hotel location,
Japanese holidays, weekends, and peak periods. Rank one to three candidates by
family fit, route efficiency, booking confidence, language accessibility,
cancellation flexibility, weather risk, and value rather than discount alone.

Compare total party prices after mandatory taxes and fees while preserving the
original currency. If a common-currency estimate materially helps, label it as
approximate and record the exchange-rate source and check date.

## Compare booking channels

For duplicate activities, show channel and direct link, date/time and
availability, original price, total party price including mandatory taxes and
fees, approximate common-currency price and exchange-rate source when used,
inclusions and exclusions, language and family restrictions, cancellation and
weather terms, booking confidence, check date, and a recommended channel with
a short reason. Do not assume the official operator is cheapest or best.

## Preserve booking state

A searchable or purchasable listing is only a candidate. Payment or a request
receipt is not confirmation. Reuse the reservation workflow's booking states.
Draft and compare freely, but obtain explicit approval before sending,
submitting, cancelling, or paying.
```

- [ ] **Step 2: Route experience requests from the main skill**

Add this row to `SKILL.md` under `Route by need`:

```markdown
| Activities, tours, tickets, workshops, factory visits, platform comparison | [experience planning](references/experience-planning.md) |
```

- [ ] **Step 3: Run focused tests and verify GREEN**

Run:

```bash
caffeinate -i -m python3 skills/japan-family-travel/tests/test_reference_contract.py -v
caffeinate -i -m python3 -m unittest tests/test_skill.py -v
```

Expected: both commands exit 0 with no failures.

- [ ] **Step 4: Refactor for concise wording**

Remove duplication between `SKILL.md` and the reference while retaining every
required phrase. Keep the main skill below 500 lines and the new reference
focused on reusable judgment rather than platform-specific UI instructions.

- [ ] **Step 5: Re-run the focused tests after refactoring**

Run the two focused commands from Step 3 again. Expected: both exit 0.

---

### Task 3: Verify, commit, and create a durable recovery artifact

**Files:**
- Verify: `skills/japan-family-travel/`
- Commit: all Task 1–2 files
- Create: a durable bundle named with the verified feature commit's short SHA

**Interfaces:**
- Consumes: the complete experience-planning implementation.
- Produces: verified package behavior, one focused commit, and a durable Git bundle reachable from the canonical clone.

- [ ] **Step 1: Run full repository and packaged verification**

Run:

```bash
caffeinate -i -m python3 -m unittest discover -s tests -v
caffeinate -i -m python3 skills/japan-family-travel/tests/test_reference_contract.py -v
```

Expected: all tests pass; the installed-link test may be skipped unless its
opt-in environment is set.

- [ ] **Step 2: Run the installed-link contract when the canonical symlink exists**

If `$HOME/.codex/skills/japan-family-travel` is a symlink to the
canonical package, run:

```bash
JFT_REQUIRE_INSTALLED_LINK=1 \
JFT_INSTALLED_LINK=$HOME/.codex/skills/japan-family-travel \
caffeinate -i -m python3 -m unittest discover -s tests -v
```

Expected: all tests pass with no installed-link skip.

- [ ] **Step 3: Run the system skill validator and whitespace check**

Run:

```bash
caffeinate -i -m python3 $HOME/.codex/skills/.system/skill-creator/scripts/quick_validate.py skills/japan-family-travel
git diff --check
```

Expected: validator success and no whitespace errors.

- [ ] **Step 4: Review scope and privacy**

Inspect `git diff --stat`, `git diff`, and `git status --short`. Relative to the
implementation branch base, confirm only the two tests, `SKILL.md`, and the new
anonymous reference changed. Confirm no real trip details, credentials, private
path, platform automation, or unrelated edits entered the skill package.

- [ ] **Step 5: Commit the independently reviewable feature**

```bash
git add tests/test_skill.py \
  skills/japan-family-travel/tests/test_reference_contract.py \
  skills/japan-family-travel/SKILL.md \
  skills/japan-family-travel/references/experience-planning.md
git commit -m "feat: add family experience planning"
```

- [ ] **Step 6: Create and verify the durable bundle**

```bash
JFT_COMMON_DIR="$(git rev-parse --path-format=absolute --git-common-dir)"
JFT_CANONICAL_REPO="$(dirname "$JFT_COMMON_DIR")"
JFT_CHECKPOINT_DIR="$(dirname "$JFT_CANONICAL_REPO")/japan-family-travel-checkpoints"
JFT_CHECKPOINT_SHA="$(git rev-parse --short HEAD)"
JFT_BUNDLE="$JFT_CHECKPOINT_DIR/japan-family-travel-experience-planning-$JFT_CHECKPOINT_SHA.bundle"
mkdir -p "$JFT_CHECKPOINT_DIR"
git -C "$JFT_CANONICAL_REPO" bundle create "$JFT_BUNDLE" feat/experience-planning
git bundle verify "$JFT_BUNDLE"
git bundle list-heads "$JFT_BUNDLE"
```

Expected: verification reports a complete bundle and `list-heads` reports
`refs/heads/feat/experience-planning` at the verified feature commit.

---

### Task 4: Complete the development branch

**Files:**
- Verify: the complete feature branch
- Preserve or integrate: `feat/experience-planning` according to the user's choice

**Interfaces:**
- Consumes: the verified feature commit and durable bundle from Task 3.
- Produces: an explicitly chosen merge, PR, preserved branch, or confirmed discard outcome.

- [ ] **Step 1: Invoke the branch-completion workflow**

Announce and use `finishing-a-development-branch`. Re-run the full repository
suite through `caffeinate -i -m`, detect the worktree and base branch, and
present the workflow's exact options. Do not merge, push, delete, or clean up
before the user chooses.

- [ ] **Step 2: Release power protection while waiting for the choice**

Before yielding to the user, terminate the tracked orchestration-scoped
`caffeinate -i` assertion. Keep the observation active because branch handling
is not complete.

- [ ] **Step 3: Execute the selected branch outcome**

After the user responds, start a new tracked orchestration-scoped
`caffeinate -i` assertion and follow `finishing-a-development-branch` exactly.
For a local merge, verify the complete suite again on the merged `main` before
cleanup. Never configure or push a remote without explicit authorization.

- [ ] **Step 4: Finish observation and release power protection**

Finish the existing observation only after the selected branch outcome is
complete, including its verification. Record the feature commit, bundle label,
verification evidence, and merge or preservation outcome. Then terminate the
tracked `caffeinate -i` assertion and confirm no scoped assertion remains.
