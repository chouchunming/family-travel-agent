from __future__ import annotations

import os
import pathlib
import re
import subprocess
import sys
import unittest

ROOT = pathlib.Path(__file__).resolve().parents[1]
CANONICAL = ROOT / "skills" / "family-travel-agent"
LEGACY = ROOT / "skills" / "japan-family-travel"


class RepositoryContractTests(unittest.TestCase):
    def test_public_shell_exists(self):
        for name in ("README.md", "LICENSE", "AGENTS.md", ".gitignore"):
            self.assertTrue((ROOT / name).is_file(), name)

    def test_mit_license(self):
        text = (ROOT / "LICENSE").read_text(encoding="utf-8")
        self.assertIn("MIT License", text)
        self.assertIn("Permission is hereby granted", text)

    def test_no_remote(self):
        result = subprocess.run(
            ["git", "remote"], cwd=ROOT, capture_output=True, text=True, check=True
        )
        self.assertEqual(result.stdout.strip(), "")


class PackageContractTests(unittest.TestCase):
    def test_canonical_packaged_contract_passes(self):
        contract = CANONICAL / "tests" / "test_reference_contract.py"
        self.assertTrue(contract.is_file(), contract)
        result = subprocess.run(
            [sys.executable, str(contract), "-v"], cwd=ROOT,
            capture_output=True, text=True, check=False,
        )
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)

    def test_legacy_is_only_a_compatibility_router(self):
        relative = {
            path.relative_to(LEGACY).as_posix()
            for path in LEGACY.rglob("*")
            if path.is_file() and "__pycache__" not in path.parts
        }
        self.assertEqual(relative, {"SKILL.md", "agents/openai.yaml"})
        skill = (LEGACY / "SKILL.md").read_text(encoding="utf-8")
        self.assertIn("canonical implementation is", skill)
        self.assertIn("`family-travel-agent`", skill)
        self.assertIn("Japan destination module", skill)

    def test_canonical_package_shape(self):
        expected = {
            "SKILL.md",
            "agents/openai.yaml",
            "references/evidence-and-needs-discovery.md",
            "references/experience-planning.md",
            "references/itinerary-workflow.md",
            "references/reservation-workflow.md",
            "references/shopping-and-dining.md",
            "references/traveler-profile-and-history.md",
            "references/versioned-trip-plans-and-budgets.md",
            "references/destinations/index.md",
            "references/destinations/japan.md",
            "tests/test_reference_contract.py",
        }
        actual = {
            path.relative_to(CANONICAL).as_posix()
            for path in CANONICAL.rglob("*")
            if path.is_file() and "__pycache__" not in path.parts
        }
        self.assertEqual(actual, expected)
        self.assertFalse((CANONICAL / "scripts").exists())

    def test_core_does_not_embed_japan_assumptions(self):
        forbidden = ("Mapcode", "ETC", "Golden Week", "Obon", "Japanese address")
        for path in CANONICAL.rglob("*.md"):
            if "destinations" in path.parts:
                continue
            text = path.read_text(encoding="utf-8")
            for token in forbidden:
                self.assertNotIn(token, text, path)


class DocumentationAndPrivacyTests(unittest.TestCase):
    def test_readme_explains_canonical_and_compatibility_invocation(self):
        text = (ROOT / "README.md").read_text(encoding="utf-8")
        for phrase in (
            "$family-travel-agent",
            "$japan-family-travel",
            "compatibility entry",
            "## Optional LLMWiki integration",
            "only after explicit confirmation",
            "does not silently persist personal data",
        ):
            self.assertIn(phrase, text)

    def test_public_candidates_are_text_without_private_data(self):
        result = subprocess.run(
            ["git", "ls-files", "-z", "--cached", "--others", "--exclude-standard"],
            cwd=ROOT, capture_output=True, check=True,
        )
        candidates = [
            item.decode("utf-8") for item in result.stdout.split(b"\0") if item
        ]
        patterns = (
            re.compile(r"/(?:Users|home)/[^/\s]+/"),
            re.compile(r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}"),
            re.compile(r"(?i)(?:booking|reservation)[ _-]?(?:id|reference)\s*[:#]\s*[A-Z0-9-]{6,}"),
            re.compile(r"(?<!\d)(?:\+\d{1,3}[- ]?)?(?:\d[- ]?){9,}(?!\d)"),
            re.compile(r"(?i)(?:auth_key|access_token|booking_token)="),
        )
        for relative in candidates:
            path = ROOT / relative
            if not path.is_file() or "__pycache__" in path.parts:
                continue
            data = path.read_bytes()
            self.assertNotIn(b"\0", data, relative)
            text = data.decode("utf-8")
            for pattern in patterns:
                self.assertIsNone(pattern.search(text), relative)


class InstalledLinkTests(unittest.TestCase):
    @unittest.skipUnless(
        os.environ.get("FTA_REQUIRE_INSTALLED_LINK") == "1",
        "installation check is opt-in",
    )
    def test_global_link_resolves_to_canonical_package(self):
        configured = os.environ.get("FTA_INSTALLED_LINK")
        self.assertIsNotNone(configured)
        installed = pathlib.Path(configured).expanduser()
        self.assertTrue(installed.is_symlink(), installed)
        self.assertEqual(installed.resolve(), CANONICAL.resolve())


if __name__ == "__main__":
    unittest.main()
