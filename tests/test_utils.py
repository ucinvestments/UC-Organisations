"""Tests for common utilities."""

import importlib.util
import sys
import unittest
from pathlib import Path

UTILS_PATH = Path(__file__).resolve().parents[1] / "common" / "utils.py"
_spec = importlib.util.spec_from_file_location("common.utils", UTILS_PATH)
utils = importlib.util.module_from_spec(_spec)
assert _spec and _spec.loader  # pragma: no cover - sanity check
_spec.loader.exec_module(utils)  # type: ignore[attr-defined]
sys.modules.setdefault("common.utils", utils)
normalize_name = utils.normalize_name


class NormalizeNameTests(unittest.TestCase):
    """Ensure normalize_name produces slug-safe tokens."""

    def test_basic_spacing(self):
        self.assertEqual(
            normalize_name("Office of the President"),
            "office_of_the_president",
        )

    def test_ampersands_and_punctuation(self):
        self.assertEqual(
            normalize_name("Investments & Strategies, Inc."),
            "investments_and_strategies_inc",
        )

    def test_diacritics_and_hyphens(self):
        self.assertEqual(
            normalize_name("José Álvarez-Rodríguez"),
            "jose_alvarez_rodriguez",
        )

    def test_empty_and_none_input(self):
        self.assertEqual(normalize_name(""), "unknown")
        self.assertEqual(normalize_name(None), "unknown")


if __name__ == "__main__":
    unittest.main()
