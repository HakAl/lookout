"""Exercise drift and path failures using disposable installs."""

import hashlib
import json
import os
from pathlib import Path
import tempfile
import unittest

from verify_skills import verify, verify_at


class VerifySkillsTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.root = Path(self.tmp.name)
        self.skill = self.root / ".agents/skills/lookout-example"
        self.skill.mkdir(parents=True)
        (self.root / "skills").mkdir()
        self.file = self.skill / "SKILL.md"
        self.file.write_text("reviewed instructions\n")
        self.lock = {"schema_version": 1, "packages": [{"name": "lookout-example",
            "files": {"SKILL.md": hashlib.sha256(self.file.read_bytes()).hexdigest()}}]}
        self.save_lock()

    def save_lock(self):
        (self.root / "skills/lock.json").write_text(json.dumps(self.lock))

    def test_exact_install(self):
        self.assertEqual([], verify(self.root))

    def held(self):
        fd = os.open(self.root, os.O_RDONLY)
        self.addCleanup(os.close, fd)
        return fd

    def test_descriptor_check_agrees_and_restores_working_directory(self):
        before = os.getcwd()
        self.assertEqual([], verify_at(self.held()))
        self.assertEqual(before, os.getcwd())
        self.file.write_text("different instructions\n")
        self.assertEqual(verify(self.root), verify_at(self.held()))
        self.assertTrue(any("Changed file" in e for e in verify_at(self.held())))
        self.assertEqual(before, os.getcwd())

    def test_descriptor_check_follows_the_directory_not_its_path(self):
        fd = self.held()
        self.file.write_text("different instructions\n")
        moved = self.root.with_name(self.root.name + "-moved")
        self.root.rename(moved)
        self.addCleanup(moved.rename, self.root)
        self.assertTrue(any("Changed file" in e for e in verify_at(fd)))

    def test_changed_bytes(self):
        self.file.write_text("different instructions\n")
        self.assertTrue(any("Changed file" in e for e in verify(self.root)))

    def test_missing_reference(self):
        self.file.unlink()
        self.assertTrue(any("Missing file" in e for e in verify(self.root)))

    def test_added_hidden_script(self):
        (self.skill / ".run.py").write_text("pass\n")
        self.assertTrue(any("Unreviewed file" in e for e in verify(self.root)))

    def test_added_package(self):
        (self.skill.parent / "unreviewed").mkdir()
        self.assertTrue(any("Unreviewed package" in e for e in verify(self.root)))

    def test_source_symlink(self):
        outside = self.root / "other.md"
        outside.write_bytes(self.file.read_bytes())
        self.file.unlink()
        self.file.symlink_to(outside)
        self.assertTrue(any("Non-regular" in e for e in verify(self.root)))

    def test_directory_symlink(self):
        (self.skill / "references").symlink_to(self.root / "skills", target_is_directory=True)
        self.assertTrue(any("Symlink directory" in e for e in verify(self.root)))

    def test_manifest_escape(self):
        self.lock["packages"][0]["files"]["../../outside"] = "0" * 64
        self.save_lock()
        self.assertTrue(any("Invalid skills/lock" in e for e in verify(self.root)))


if __name__ == "__main__":
    unittest.main()
