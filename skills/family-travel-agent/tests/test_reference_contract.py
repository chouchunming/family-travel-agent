from __future__ import annotations

import pathlib
import re
import unittest

SKILL_ROOT = pathlib.Path(__file__).resolve().parents[1]
SKILL_MD = SKILL_ROOT / "SKILL.md"
AGENT_YAML = SKILL_ROOT / "agents" / "openai.yaml"
CORE_REFERENCES = (
    "evidence-and-needs-discovery.md",
    "experience-planning.md",
    "family-itinerary-pdf-layout.md",
    "itinerary-workflow.md",
    "reservation-workflow.md",
    "shopping-and-dining.md",
    "traveler-profile-and-history.md",
    "versioned-trip-plans-and-budgets.md",
)


class ReferenceContractTests(unittest.TestCase):
    def test_frontmatter_and_metadata(self):
        skill = SKILL_MD.read_text(encoding="utf-8")
        self.assertTrue(skill.startswith("---\nname: family-travel-agent\n"))
        metadata = AGENT_YAML.read_text(encoding="utf-8")
        self.assertIn('display_name: "Family Travel Agent"', metadata)
        self.assertIn("$family-travel-agent", metadata)
        self.assertIn("allow_implicit_invocation: true", metadata)

    def test_router_links_all_core_references_and_destination_index(self):
        skill = SKILL_MD.read_text(encoding="utf-8")
        for name in CORE_REFERENCES:
            self.assertIn(f"references/{name}", skill)
            self.assertTrue((SKILL_ROOT / "references" / name).is_file(), name)
        self.assertIn("references/destinations/index.md", skill)

    def test_modes_privacy_and_action_gate(self):
        skill = SKILL_MD.read_text(encoding="utf-8")
        normalized = " ".join(skill.split())
        for phrase in (
            "Standalone mode",
            "LLMWiki-enhanced mode",
            "wiki_cli.py",
            "user-provided path",
            "detection is incomplete",
            "one dedicated private-data file per project",
            "fail closed",
            "Public and sanitized generation must be independent",
            "explicit approval",
            "external action",
        ):
            self.assertIn(phrase, normalized)

    def test_unsupported_destination_discovery_is_explicit(self):
        index = (SKILL_ROOT / "references" / "destinations" / "index.md")
        self.assertTrue(index.is_file())
        text = index.read_text(encoding="utf-8")
        normalized = " ".join(text.split())
        for phrase in (
            "Unsupported-destination discovery",
            "do not borrow another destination's conventions",
            "current primary official sources",
            "verification date",
            "missing module",
            "multi-country trip",
        ):
            self.assertIn(phrase, normalized)

    def test_japan_module_owns_local_conventions(self):
        module = SKILL_ROOT / "references" / "destinations" / "japan.md"
        self.assertTrue(module.is_file())
        text = module.read_text(encoding="utf-8")
        for phrase in (
            "Cabinet Office",
            "Golden Week",
            "Obon",
            "ETC",
            "Mapcode",
            "Japanese address",
            "driving credential",
            "Amazon.co.jp",
            "Japan Tourism Agency",
            "National Tax Agency",
        ):
            self.assertIn(phrase, text)

    def test_core_has_no_japan_only_tokens(self):
        forbidden = ("Mapcode", "ETC", "Golden Week", "Obon", "Japanese address")
        for path in SKILL_ROOT.rglob("*.md"):
            if "destinations" in path.parts:
                continue
            text = path.read_text(encoding="utf-8")
            for token in forbidden:
                self.assertNotIn(token, text, str(path))

    def test_no_private_path_or_embedded_trip(self):
        for path in SKILL_ROOT.rglob("*"):
            if (
                not path.is_file()
                or "__pycache__" in path.parts
                or "tests" in path.parts
            ):
                continue
            text = path.read_text(encoding="utf-8")
            self.assertIsNone(re.search(r"/(?:Users|home)/[^/\s]+/", text), path)
            self.assertNotIn("Nagoya", text, path)


if __name__ == "__main__":
    unittest.main()
