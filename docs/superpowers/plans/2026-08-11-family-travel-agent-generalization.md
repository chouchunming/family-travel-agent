# Family Travel Agent Generalization Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use
> superpowers:subagent-driven-development (recommended) or
> superpowers:executing-plans to implement this plan task-by-task. Steps use
> checkbox (`- [ ]`) syntax for tracking.

**Goal:** Make `family-travel-agent` the destination-neutral canonical skill,
with Japan as its first destination module and `japan-family-travel` retained
as a compatibility router.

**Architecture:** The canonical skill owns all cross-destination workflow and
privacy rules. Destination modules own local law, transport, navigation,
holiday, tax, payment, cultural, and reservation conventions. The legacy skill
contains no duplicate workflow and forwards Japan requests to the canonical
skill plus the Japan module.

**Tech Stack:** Markdown Agent Skills, OpenAI skill metadata YAML, Python
`unittest` static contract tests, optional LLMWiki task records.

## Global Constraints

- Keep the repository dependency-free and do not add scripts or package files.
- Only anonymous examples may be tracked; no real trip or traveler data.
- Do not commit, push, publish, book, purchase, send, or change remote state.
- Run any authorized validation on macOS through `caffeinate -i -m`.
- Keep sensitive Python values in one local, Git-ignored private-data file per
  project; sanitized builds must not depend on it.
- Mark the Wiki task complete only after implementation and validation pass.

---

## File map

**Create canonical package**

- `skills/family-travel-agent/SKILL.md`: authoritative router and boundaries.
- `skills/family-travel-agent/agents/openai.yaml`: canonical discovery metadata.
- `skills/family-travel-agent/references/evidence-and-needs-discovery.md`:
  evidence hierarchy and optional LLMWiki mode.
- `skills/family-travel-agent/references/experience-planning.md`: activity and
  booking-channel comparison.
- `skills/family-travel-agent/references/itinerary-workflow.md`: neutral daily
  feasibility and destination-calendar pass.
- `skills/family-travel-agent/references/reservation-workflow.md`: booking
  states and action gate.
- `skills/family-travel-agent/references/shopping-and-dining.md`: route-aware,
  destination-neutral selection.
- `skills/family-travel-agent/references/traveler-profile-and-history.md`:
  private family profile and history handling.
- `skills/family-travel-agent/references/versioned-trip-plans-and-budgets.md`:
  immutable trip versions and ledgers.
- `skills/family-travel-agent/references/destinations/index.md`: module registry
  and unsupported-destination discovery contract.
- `skills/family-travel-agent/references/destinations/japan.md`: Japan-only
  holidays, driving, Mapcode, parking, tax-free, accommodation, dining, and
  reservation conventions.
- `skills/family-travel-agent/tests/test_reference_contract.py`: packaged
  canonical contract.

**Convert compatibility package**

- Modify `skills/japan-family-travel/SKILL.md` into a compatibility router.
- Modify `skills/japan-family-travel/agents/openai.yaml` for legacy discovery.
- Delete `skills/japan-family-travel/references/*.md` after their neutral rules
  are represented canonically and Japan rules are moved to the Japan module.
- Delete `skills/japan-family-travel/tests/test_reference_contract.py` because
  the legacy package no longer owns a separate reference contract.

**Repository and Wiki**

- Modify `tests/test_skill.py` for canonical and compatibility contracts.
- Modify `README.md` for neutral invocation and compatibility instructions.
- Create installed link `~/.codex/skills/family-travel-agent` pointing to the
  canonical package while preserving the legacy link.
- Modify `wiki/tasks/records/travel-generalize-family-travel-agent.md` only
  after validation, then regenerate task dashboards.

---

### Task 1: Define failing architecture contracts

**Files:**

- Modify: `tests/test_skill.py`
- Create: `skills/family-travel-agent/tests/test_reference_contract.py`

**Interfaces:**

- Produces: static package layout, neutrality, compatibility, privacy, and
  destination-module contracts used by all later tasks.

- [ ] **Step 1: Replace the single-skill constants**

```python
ROOT = pathlib.Path(__file__).resolve().parents[1]
CANONICAL = ROOT / "skills" / "family-travel-agent"
LEGACY = ROOT / "skills" / "japan-family-travel"
```

- [ ] **Step 2: Add repository architecture tests**

```python
def test_canonical_and_legacy_packages_exist(self):
    self.assertTrue((CANONICAL / "SKILL.md").is_file())
    self.assertTrue((LEGACY / "SKILL.md").is_file())

def test_legacy_is_only_a_compatibility_router(self):
    relative = {
        path.relative_to(LEGACY).as_posix()
        for path in LEGACY.rglob("*")
        if path.is_file() and "__pycache__" not in path.parts
    }
    self.assertEqual(relative, {"SKILL.md", "agents/openai.yaml"})

def test_core_does_not_embed_japan_assumptions(self):
    forbidden = ("Mapcode", "ETC", "Golden Week", "Obon", "Japanese address")
    for path in CANONICAL.rglob("*.md"):
        if "destinations" in path.parts:
            continue
        text = path.read_text(encoding="utf-8")
        for token in forbidden:
            self.assertNotIn(token, text, path)
```

- [ ] **Step 3: Add the packaged canonical contract**

The packaged test must assert exact frontmatter and metadata, links to all core
references and `destinations/index.md`, an explicit unsupported-destination
workflow, the private-data isolation rule, the external-action approval gate,
optional LLMWiki detection, Japan module existence, and Japan module ownership
of `Mapcode`, `ETC`, `Golden Week`, `Obon`, `Japanese address`, and driving
credential guidance.

- [ ] **Step 4: Run the focused tests only after validation permission**

```bash
caffeinate -i -m python3 -m unittest \
  skills/family-travel-agent/tests/test_reference_contract.py -v
```

Expected before implementation: failures for missing canonical files.

---

### Task 2: Create the canonical skill router and metadata

**Files:**

- Create: `skills/family-travel-agent/SKILL.md`
- Create: `skills/family-travel-agent/agents/openai.yaml`

**Interfaces:**

- Consumes: reference names fixed by Task 1.
- Produces: canonical `$family-travel-agent` invocation and reference routing.

- [ ] **Step 1: Create canonical frontmatter and workflow**

Use this frontmatter:

```yaml
---
name: family-travel-agent
description: Use when planning or maintaining family travel across one or more destinations, including itineraries, transport, reservations, activities, dining, shopping, budgets, traveler preferences, trip history, and local travel communication.
---
```

The body must define explicit scope discovery, standalone and optional
LLMWiki-enhanced modes, destination-module selection, unsupported-destination
discovery, verified-fact versus recommendation labels, versioned artifacts,
privacy isolation, and exact approval before external actions.

- [ ] **Step 2: Link every canonical reference**

The router must link the seven neutral references,
`references/versioned-trip-plans-and-budgets.md`, and
`references/destinations/index.md`. It must instruct Japan trips to load
`references/destinations/japan.md` through the index rather than embedding
Japan rules in the router.

- [ ] **Step 3: Create canonical metadata**

```yaml
interface:
  display_name: "Family Travel Agent"
  short_description: "Plan family travel across destinations"
  default_prompt: "Use $family-travel-agent to plan this family trip from confirmed preferences, destination modules, and current evidence."
policy:
  allow_implicit_invocation: true
```

---

### Task 3: Build neutral references and the Japan module

**Files:**

- Create: all canonical files listed under **Create canonical package**.

**Interfaces:**

- Consumes: reference routes from Task 2.
- Produces: destination-neutral planning behavior plus the Japan adapter.

- [ ] **Step 1: Carry forward already-neutral contracts**

Preserve the existing evidence hierarchy, experience comparison, reservation
states, version lineage, budget ledger, and optional LLMWiki behavior. Replace
language-specific communication with `local language or English`.

- [ ] **Step 2: Generalize itinerary, profile, shopping, and dining rules**

Move holiday names, local store catalogs, tax-free rules, onsen/room vocabulary,
Mapcode, and Japanese address handling out of core references. Core fields use
`destination holiday`, `local peak period`, `navigation identifier`, `local
driving credential`, `accommodation format`, and `destination tax/refund rule`.

- [ ] **Step 3: Create the module registry**

`destinations/index.md` must list Japan as supported and define this fallback:

```text
If no module exists, do not borrow another destination's conventions. Check
current official sources for entry, driving, transport, holidays, taxes,
payments, safety, reservations, accessibility, and language. Record source,
check date, confidence, and open loops.
```

- [ ] **Step 4: Create the Japan module**

The Japan module must preserve current Japan-specific behavior: Cabinet Office
holiday checks, Golden Week/Obon/New Year demand periods, Mapcode target and
fallback rules, Japanese address and telephone navigation, ETC/tolls, local
driving-document verification, parking entrances, accommodation meal plans and
bathing formats, reservation names, Japanese communication, route-aware local
shopping/dining, hotel delivery, and current official tax-free checks.

---

### Task 4: Convert the old skill to a compatibility router

**Files:**

- Modify: `skills/japan-family-travel/SKILL.md`
- Modify: `skills/japan-family-travel/agents/openai.yaml`
- Delete: legacy `references/*.md`
- Delete: legacy `tests/test_reference_contract.py`

**Interfaces:**

- Consumes: canonical skill and Japan module from Tasks 2 and 3.
- Produces: backward-compatible `$japan-family-travel` discovery without
  duplicate rules.

- [ ] **Step 1: Replace the legacy body**

The compatibility body must state that `family-travel-agent` is canonical,
require loading its full workflow and Japan destination module, preserve the
same privacy/action boundaries, and fail visibly if the canonical skill is not
installed. It must not copy canonical planning steps.

- [ ] **Step 2: Replace legacy metadata**

```yaml
interface:
  display_name: "Japan Family Travel (Compatibility)"
  short_description: "Route Japan trips to Family Travel Agent"
  default_prompt: "Use $japan-family-travel as the compatibility entry for $family-travel-agent with the Japan destination module."
policy:
  allow_implicit_invocation: true
```

- [ ] **Step 3: Remove duplicate legacy references and packaged tests**

Delete only the files listed in the file map. Keep the legacy directory,
`SKILL.md`, and metadata.

---

### Task 5: Update repository documentation and installation

**Files:**

- Modify: `README.md`
- Create symlink: `~/.codex/skills/family-travel-agent`

**Interfaces:**

- Produces: user-facing canonical invocation and installed skill discovery.

- [ ] **Step 1: Rewrite README identity and usage**

Document `$family-travel-agent` as canonical for all destinations, explain the
Japan module and legacy invocation, retain standalone/LLMWiki modes, privacy,
explicit external-action approval, anonymous examples, and development command.

- [ ] **Step 2: Install the canonical link**

Create a symlink from `~/.codex/skills/family-travel-agent` to
`skills/family-travel-agent`. Refuse to overwrite a non-symlink or a symlink
that targets another package; preserve the existing Japan link.

---

### Task 6: Validate and close the Wiki task

**Files:**

- Modify after validation:
  `wiki/tasks/records/travel-generalize-family-travel-agent.md`
- Regenerate: Wiki task dashboards through `wiki_cli.py tasks`.

**Interfaces:**

- Consumes: completed repository implementation.
- Produces: validated installed skills and a completed canonical open loop.

- [ ] **Step 1: Run validation only after explicit permission**

```bash
caffeinate -i -m python3 -m unittest discover -s tests -v
caffeinate -i -m python3 \
  $CODEX_HOME/skills/.system/skill-creator/scripts/quick_validate.py \
  skills/family-travel-agent
caffeinate -i -m python3 \
  $CODEX_HOME/skills/.system/skill-creator/scripts/quick_validate.py \
  skills/japan-family-travel
```

Expected: all repository tests pass and both skill validations report valid.

- [ ] **Step 2: Complete and regenerate the Wiki task**

Set `status: completed`, clear `next_action`, add `completed_at: 2026-08-11`,
and summarize the canonical skill, compatibility entry, and Japan module in the
task body. Then run:

```bash
caffeinate -i -m python3 wiki_cli.py tasks
caffeinate -i -m python3 wiki_cli.py lint
```

Expected: generated task dashboards no longer list this item as pending and
Wiki lint reports no new task error.

- [ ] **Step 3: Report without Git side effects**

Provide the canonical and compatibility paths, validation evidence, Wiki task
status, and any pre-existing unrelated warning. Do not commit or publish.
