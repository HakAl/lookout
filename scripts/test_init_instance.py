"""Exercise instance creation on disposable copies of the real templates."""

import contextlib
import io
import os
from pathlib import Path
import re
import shutil
import sys
import tempfile
import unittest
from unittest import mock

import init_instance

ROOT = Path(__file__).resolve().parents[1]
DESTINATIONS = [destination for _, destination, _ in init_instance.INSTANCE_FILES]
LINK = re.compile(r"\]\(([^)#]+)(?:#[^)]*)?\)")


class InitInstanceTests(unittest.TestCase):
    def setUp(self):
        tmp = tempfile.TemporaryDirectory()
        self.addCleanup(tmp.cleanup)
        self.root = Path(tmp.name)
        shutil.copytree(ROOT / "templates", self.root / "templates")

    def run_main(self):
        out, err = io.StringIO(), io.StringIO()
        argv = ["init_instance.py", "--root", str(self.root)]
        with mock.patch.object(sys, "argv", argv), \
                contextlib.redirect_stdout(out), contextlib.redirect_stderr(err):
            code = init_instance.main()
        return code, out.getvalue(), err.getvalue()

    def test_creates_every_instance_file(self):
        created, kept, errors = init_instance.init(self.root)
        self.assertEqual(DESTINATIONS, created)
        self.assertEqual(([], []), (kept, errors))
        for destination in DESTINATIONS:
            self.assertTrue((self.root / destination).is_file(), destination)

    def test_existing_files_are_not_overwritten(self):
        (self.root / "TEAM.md").write_text("my team\n")
        created, kept, errors = init_instance.init(self.root)
        self.assertEqual(["TEAM.md"], kept)
        self.assertNotIn("TEAM.md", created)
        self.assertEqual([], errors)
        self.assertEqual("my team\n", (self.root / "TEAM.md").read_text())

    def complete_kit(self):
        shutil.copytree(ROOT / ".agents", self.root / ".agents")
        shutil.copytree(ROOT / "skills", self.root / "skills")

    def outside_dir(self):
        tmp = tempfile.TemporaryDirectory()
        self.addCleanup(tmp.cleanup)
        return Path(tmp.name)

    def test_dangling_symlink_is_an_error_and_is_not_replaced(self):
        link = self.root / "QUEUE.md"
        link.symlink_to(self.root / "absent")
        created, kept, errors = init_instance.init(self.root)
        self.assertNotIn("QUEUE.md", created + kept)
        self.assertTrue(any("QUEUE.md" in e for e in errors))
        self.assertTrue(link.is_symlink())
        self.assertFalse((self.root / "absent").exists())

    def test_symlink_to_a_real_file_is_an_error(self):
        outside = self.outside_dir() / "team.md"
        outside.write_text("elsewhere\n")
        (self.root / "TEAM.md").symlink_to(outside)
        created, kept, errors = init_instance.init(self.root)
        self.assertNotIn("TEAM.md", created + kept)
        self.assertEqual(1, len(errors))
        self.assertEqual("elsewhere\n", outside.read_text())

    def test_unusable_destinations_fail_the_command_on_a_complete_kit(self):
        # Skills are intact, so only the instance paths can cause the failure.
        self.complete_kit()
        (self.root / "TEAM.md").mkdir()
        (self.root / "QUEUE.md").symlink_to(self.root / "absent")
        code, out, err = self.run_main()
        self.assertEqual(1, code)
        self.assertIn("Installed skills match the lock.", out)
        self.assertIn("TEAM.md exists but is not a regular file", err)
        self.assertIn("QUEUE.md exists but is not a regular file", err)
        self.assertNotIn("Next:", out)
        self.assertTrue((self.root / "TEAM.md").is_dir())

    def test_symlinked_projects_directory_is_not_written_through(self):
        outside = self.outside_dir()
        (self.root / "projects").symlink_to(outside, target_is_directory=True)
        created, _, errors = init_instance.init(self.root)
        self.assertNotIn("projects/INDEX.md", created)
        self.assertTrue(any("projects/INDEX.md" in e for e in errors))
        self.assertEqual([], list(outside.iterdir()))

    def test_symlinked_templates_directory_is_not_read_through(self):
        outside = self.outside_dir()
        shutil.copytree(self.root / "templates", outside / "templates")
        shutil.rmtree(self.root / "templates")
        (self.root / "templates").symlink_to(outside / "templates", target_is_directory=True)
        created, _, errors = init_instance.init(self.root)
        self.assertEqual([], created)
        self.assertEqual(4, len(errors))
        self.assertFalse((self.root / "TEAM.md").exists())

    def test_symlinked_template_file_is_not_read_through(self):
        outside = self.outside_dir() / "planted.md"
        outside.write_text("planted\n")
        (self.root / "templates/TEAM.md").unlink()
        (self.root / "templates/TEAM.md").symlink_to(outside)
        created, _, errors = init_instance.init(self.root)
        self.assertNotIn("TEAM.md", created)
        self.assertEqual(1, len(errors))
        self.assertFalse((self.root / "TEAM.md").exists())

    def test_failed_write_leaves_nothing_and_a_retry_completes(self):
        self.complete_kit()
        real_write = os.write

        def partial_then_fail(fd, data):
            real_write(fd, bytes(data[:10]))
            raise OSError(28, "No space left on device")

        with mock.patch.object(init_instance.os, "write", partial_then_fail):
            code, out, err = self.run_main()
        self.assertEqual(1, code)
        self.assertIn("Could not create TEAM.md", err)
        self.assertNotIn("Created", out)
        leftovers = [p.name for p in self.root.iterdir() if p.name not in
                     ("templates", ".agents", "skills", "projects")]
        self.assertEqual([], leftovers)
        self.assertEqual([], list((self.root / "projects").iterdir()))

        code, out, err = self.run_main()
        self.assertEqual((0, ""), (code, err))
        for destination, (template, _, _) in zip(DESTINATIONS, init_instance.INSTANCE_FILES):
            self.assertIn(f"Created {destination}", out)
            self.assertEqual(
                (self.root / template).stat().st_size > 0,
                (self.root / destination).stat().st_size > 0,
            )
        self.assertEqual(
            (ROOT / "templates/QUEUE.md").read_text(), (self.root / "QUEUE.md").read_text()
        )

    def test_stale_temporary_file_is_neither_reused_nor_removed(self):
        stale = self.root / ".TEAM.md.init-tmp"
        stale.write_text("partial")
        created, _, errors = init_instance.init(self.root)
        self.assertIn("TEAM.md", created)
        self.assertEqual([], errors)
        self.assertEqual("partial", stale.read_text())
        self.assertEqual([".TEAM.md.init-tmp"],
                         [p.name for p in self.root.iterdir() if p.name.endswith(".init-tmp")])

    def overlap(self, inner_write):
        """Run a second init inside the first run's first write."""
        real_write = os.write
        state = {"depth": 0, "inner": None}

        def write(fd, data):
            if state["depth"] == 0 and state["inner"] is None:
                state["depth"] = 1
                with mock.patch.object(init_instance.os, "write", inner_write):
                    state["inner"] = init_instance.init(self.root)
                state["depth"] = 0
            return real_write(fd, data)

        with mock.patch.object(init_instance.os, "write", write):
            outer = init_instance.init(self.root)
        return outer, state["inner"]

    def assert_complete_instance(self):
        for (template, destination, rewrites) in init_instance.INSTANCE_FILES:
            expected = (self.root / template).read_text()
            for old, new in rewrites:
                expected = expected.replace(old, new)
            self.assertEqual(expected, (self.root / destination).read_text(), destination)
        self.assertEqual([], [p.name for p in self.root.rglob("*.init-tmp")])

    def test_overlapping_run_that_fails_midwrite_cannot_be_published(self):
        real_write = os.write

        def partial_then_fail(fd, data):
            real_write(fd, bytes(data[:10]))
            raise OSError(28, "No space left on device")

        outer, inner = self.overlap(partial_then_fail)
        self.assertEqual(4, len(inner[2]))
        self.assertEqual((DESTINATIONS, [], []), outer)
        self.assert_complete_instance()

    def test_overlapping_run_that_finishes_first_is_kept_whole(self):
        outer, inner = self.overlap(os.write)
        self.assertEqual((DESTINATIONS, [], []), inner)
        # The first run lost the race for TEAM.md and found the rest present.
        self.assertEqual(([], DESTINATIONS, []), outer)
        self.assert_complete_instance()

    def test_fifo_at_a_template_name_is_refused_without_blocking(self):
        (self.root / "templates/TEAM.md").unlink()
        os.mkfifo(self.root / "templates/TEAM.md")
        created, _, errors = init_instance.init(self.root)
        self.assertNotIn("TEAM.md", created)
        self.assertEqual(1, len(errors))
        self.assertIn("not a regular file", errors[0])

    def corrupt_a_skill(self, root):
        skill = next((root / ".agents/skills").glob("*/SKILL.md"))
        skill.write_text(skill.read_text() + "tampered\n")

    def test_root_given_through_a_link_is_pinned_before_setup_and_check(self):
        self.complete_kit()
        other = self.outside_dir()
        link = self.outside_dir() / "instance"
        link.symlink_to(self.root, target_is_directory=True)
        real_verify_at = init_instance.verify_at

        def retarget_then_verify(root_fd):
            link.unlink()
            link.symlink_to(other, target_is_directory=True)
            return real_verify_at(root_fd)

        out, err = io.StringIO(), io.StringIO()
        with mock.patch.object(sys, "argv", ["init_instance.py", "--root", str(link)]), \
                mock.patch.object(init_instance, "verify_at", retarget_then_verify), \
                contextlib.redirect_stdout(out), contextlib.redirect_stderr(err):
            code = init_instance.main()
        # Both steps used the directory the link named at the start.
        self.assertEqual((0, ""), (code, err.getvalue()))
        self.assert_complete_instance()
        self.assertEqual([], list(other.iterdir()))

    def test_root_replaced_between_setup_and_check_fails(self):
        self.complete_kit()
        moved = self.outside_dir() / "moved"
        real_verify_at = init_instance.verify_at

        def swap_then_verify(root_fd):
            # A complete kit takes the root's place after setup wrote elsewhere.
            self.root.rename(moved)
            shutil.copytree(moved, self.root)
            return real_verify_at(root_fd)

        with mock.patch.object(init_instance, "verify_at", swap_then_verify):
            code, out, err = self.run_main()
        self.assertEqual(1, code)
        self.assertIn("was replaced while this script ran", err)
        self.assertNotIn("Next:", out)

    def test_skill_check_reads_the_set_up_directory_during_a_swap_and_restore(self):
        # The instance being set up has a tampered skill. While the check runs,
        # its path names a clean kit, and the path is restored before the final
        # identity comparison. Only a check bound to the held directory fails.
        self.complete_kit()
        self.corrupt_a_skill(self.root)
        moved = self.outside_dir() / "moved"
        real_verify_at = init_instance.verify_at

        def swap_verify_restore(root_fd):
            self.root.rename(moved)
            self.root.mkdir()
            shutil.copytree(ROOT / ".agents", self.root / ".agents")
            shutil.copytree(ROOT / "skills", self.root / "skills")
            try:
                return real_verify_at(root_fd)
            finally:
                shutil.rmtree(self.root)
                moved.rename(self.root)

        with mock.patch.object(init_instance, "verify_at", swap_verify_restore):
            code, out, err = self.run_main()
        self.assertEqual(1, code)
        self.assertIn("Changed file", err)
        self.assertIn("Skill check failed", err)
        self.assertNotIn("was replaced", err)
        self.assertNotIn("Installed skills match the lock.", out)

    def test_clean_instance_passes_while_its_path_names_a_tampered_kit(self):
        # The converse: a decoy's failure must not be charged to the instance.
        self.complete_kit()
        moved = self.outside_dir() / "moved"
        real_verify_at = init_instance.verify_at

        def swap_verify_restore(root_fd):
            self.root.rename(moved)
            self.root.mkdir()
            shutil.copytree(ROOT / ".agents", self.root / ".agents")
            shutil.copytree(ROOT / "skills", self.root / "skills")
            self.corrupt_a_skill(self.root)
            try:
                return real_verify_at(root_fd)
            finally:
                shutil.rmtree(self.root)
                moved.rename(self.root)

        with mock.patch.object(init_instance, "verify_at", swap_verify_restore):
            code, out, err = self.run_main()
        self.assertEqual((0, ""), (code, err))
        self.assert_complete_instance()

    def test_second_run_changes_nothing(self):
        init_instance.init(self.root)
        before = {d: (self.root / d).read_bytes() for d in DESTINATIONS}
        created, kept, errors = init_instance.init(self.root)
        self.assertEqual(([], DESTINATIONS, []), (created, kept, errors))
        self.assertEqual(before, {d: (self.root / d).read_bytes() for d in DESTINATIONS})

    def test_missing_template_is_reported_and_others_still_created(self):
        (self.root / "templates/QUEUE.md").unlink()
        created, _, errors = init_instance.init(self.root)
        self.assertNotIn("QUEUE.md", created)
        self.assertEqual(3, len(created))
        self.assertEqual(1, len(errors))
        self.assertIn("QUEUE.md", errors[0])

    def test_relative_links_in_created_files_resolve_in_the_kit(self):
        # Checked against the real kit tree: a link the move would break fails.
        init_instance.init(self.root)
        checked = 0
        for destination in DESTINATIONS:
            text = (self.root / destination).read_text()
            for target in LINK.findall(text):
                if "://" in target or target.startswith("<"):
                    continue
                resolved = (ROOT / destination).parent / target
                self.assertTrue(resolved.exists(), f"{destination}: {target}")
                checked += 1
        self.assertGreaterEqual(checked, 4)

    def test_main_fails_when_skill_check_fails(self):
        # The disposable root has templates but no skills or lock.
        code, out, err = self.run_main()
        self.assertEqual(1, code)
        self.assertIn("Created TEAM.md", out)
        self.assertIn("Skill check failed", err)
        self.assertNotIn("Next:", out)

    def test_main_succeeds_on_a_complete_kit(self):
        self.complete_kit()
        code, out, err = self.run_main()
        self.assertEqual((0, ""), (code, err))
        self.assertIn("Installed skills match the lock.", out)
        self.assertIn("Next:", out)


if __name__ == "__main__":
    unittest.main()
