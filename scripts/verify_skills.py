#!/usr/bin/env python3
"""Check installed Lookout skills against the reviewed file inventory; no writes."""

import argparse
import hashlib
import json
from pathlib import Path, PurePosixPath
import os
import stat
import sys


def verify(root):
    root = Path(root).resolve()
    errors = []
    try:
        lock = json.loads((root / "skills/lock.json").read_text())
        if lock["schema_version"] != 1 or not lock["packages"]:
            raise ValueError("unsupported or empty lock")
        expected = {}
        names = set()
        for package in lock["packages"]:
            name = package["name"]
            if not isinstance(name, str) or not name.startswith("lookout-") or any(
                c not in "abcdefghijklmnopqrstuvwxyz0123456789-" for c in name
            ) or name in names:
                raise ValueError("invalid or duplicate package name")
            names.add(name)
            files = package["files"]
            if "SKILL.md" not in files:
                raise ValueError("package lacks SKILL.md")
            for rel, digest in files.items():
                path = PurePosixPath(rel)
                if path.is_absolute() or not path.parts or any(
                    part in (".", "..") for part in rel.split("/")
                ) or "\\" in rel or str(path) != rel:
                    raise ValueError("invalid package file path")
                if not isinstance(digest, str) or len(digest) != 64 or any(
                    c not in "0123456789abcdef" for c in digest
                ):
                    raise ValueError("invalid SHA256")
                expected[f"{name}/{rel}"] = digest
    except (OSError, ValueError, KeyError, TypeError, AttributeError) as exc:
        return [f"Invalid skills/lock.json: {exc}"]

    skill_root = root / ".agents/skills"
    if (root / ".agents").is_symlink() or skill_root.is_symlink():
        return ["Skill root must not be a symlink"]
    if not skill_root.is_dir():
        return ["Missing .agents/skills"]
    actual = set()
    for directory, dirs, files in os.walk(skill_root, followlinks=False):
        for name in list(dirs):
            path = Path(directory) / name
            if path.is_symlink():
                errors.append(f"Symlink directory: {path.relative_to(skill_root)}")
                dirs.remove(name)
        for name in files:
            path = Path(directory) / name
            rel = path.relative_to(skill_root).as_posix()
            actual.add(rel)
            try:
                mode = path.lstat().st_mode
                if not stat.S_ISREG(mode):
                    errors.append(f"Non-regular file: {rel}")
                elif rel not in expected:
                    errors.append(f"Unreviewed file: {rel}")
                elif hashlib.sha256(path.read_bytes()).hexdigest() != expected[rel]:
                    errors.append(f"Changed file: {rel}")
            except OSError as exc:
                errors.append(f"Unreadable file: {rel}: {exc}")
    errors.extend(f"Missing file: {rel}" for rel in sorted(set(expected) - actual))
    for child in skill_root.iterdir():
        if child.name not in names:
            errors.append(f"Unreviewed package or entry: {child.name}")
    return errors


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=Path(__file__).resolve().parents[1])
    args = parser.parse_args()
    errors = verify(args.root)
    for error in errors:
        print(error, file=sys.stderr)
    if errors:
        return 1
    print("Installed skills match the reviewed file inventory. No safety guarantee implied.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
