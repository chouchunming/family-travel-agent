---
name: japan-family-travel
description: Use when an existing workflow explicitly invokes the legacy Japan Family Travel skill or requests Japan-specific family itinerary, self-drive, Mapcode, reservation, dining, shopping, or travel communication support.
---

# Japan Family Travel Compatibility Entry

This is a compatibility router. The canonical implementation is
`family-travel-agent`.

When this legacy skill is invoked:

1. Load the full `family-travel-agent` skill.
2. Load its `references/destinations/index.md` and Japan destination module.
3. Follow the canonical evidence, privacy, versioning, LLMWiki, reservation,
   and explicit external-action approval boundaries.
4. Apply Japan rules only to Japan segments.

Do not reproduce or maintain a second planning workflow here. If the canonical
skill or Japan module is not installed, disclose the installation problem and
stop before applying stale or guessed destination rules.
