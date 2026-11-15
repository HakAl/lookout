"""Check the skills actually installed in this checkout against its own lock.

test_verify_skills.py exercises the verifier on synthetic installs. This test
points the same verifier at the real `.agents/skills` and `skills/lock.json` of
the tree it runs from, so a corrupted or incomplete kit fails the test command.
"""

import json
from pathlib import Path
import unittest

from verify_skills import verify

ROOT = Path(__file__).resolve().parents[1]


class KitInstallTests(unittest.TestCase):
    def test_installed_skills_match_lock(self):
        self.assertEqual([], verify(ROOT))

    def test_lock_is_portable(self):
        text = (ROOT / "skills/lock.json").read_text()
        lock = json.loads(text)
        for package in lock["packages"]:
            self.assertEqual(
                f".agents/skills/{package['name']}", package["installed_path"]
            )
            for key in ("source_root", "snapshot"):
                self.assertNotIn(key, package["source"], package["name"])
            self.assertNotIn("review_receipts", package, package["name"])
        for marker in ("/Users/", "/home/", "/Volumes/"):
            self.assertNotIn(marker, text)


if __name__ == "__main__":
    unittest.main()
