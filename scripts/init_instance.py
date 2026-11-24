#!/usr/bin/env python3
"""Create the instance files for a new Lookout seat, then check the skills.

Copies the four starting templates to their instance locations and runs the
skill integrity check. An instance file that already exists is left untouched,
so the script is safe to run again. Placeholders are not filled in; edit the
created files afterwards.

Every template and instance path is opened one component at a time beneath the
instance root without following symbolic links, so a linked `templates/` or
`projects/` cannot move a read or a write outside the root. A new file is
written under a temporary name private to this run and only then given its
final name, which never replaces an existing entry. An existing entry that is
not a regular file is reported as an error, because the seat could not read it.

The root is opened once. Setup and the skill check both read and write through
that one descriptor, so the exit status describes a single directory even if
the path is pointed elsewhere while the script runs. The command also fails if
the path no longer names that directory at the end.

Exit codes: 0 all four instance files are regular files and the skills match
the lock, 1 otherwise.

Python 3.9+, standard library only. Needs an operating system where Python can
open paths relative to a directory descriptor (Linux, macOS and other Unix).
"""

import argparse
import os
from pathlib import Path
import secrets
import stat
import sys

from verify_skills import verify_at

# template, destination, link rewrites needed because the file moves.
INSTANCE_FILES = (
    ("templates/TEAM.md", "TEAM.md", (("](../", "]("),)),
    ("templates/QUEUE.md", "QUEUE.md", (("](../", "]("),)),
    ("templates/TOOLS.local.md", "TOOLS.local.md", (("](../", "]("),)),
    (
        "templates/projects-index.md",
        "projects/INDEX.md",
        (("](project.md)", "](../templates/project.md)"),),
    ),
)

_NEEDED = (os.open, os.mkdir, os.stat, os.unlink, os.link)
_UNSUPPORTED = (
    "This platform cannot open paths relative to a directory without "
    "following links. Copy the templates by hand; see templates/, then run "
    "scripts/verify_skills.py."
)
_DIR_FLAGS = os.O_RDONLY | getattr(os, "O_DIRECTORY", 0) | getattr(os, "O_NOFOLLOW", 0)


def supported():
    return (
        hasattr(os, "O_NOFOLLOW")
        and hasattr(os, "fchdir")
        and all(f in os.supports_dir_fd for f in _NEEDED)
    )


def _open_parent(root_fd, relative, create):
    """Return (fd of the parent directory, leaf name), refusing symlinks."""
    *parents, leaf = relative.split("/")
    fd = os.dup(root_fd)
    try:
        for part in parents:
            if create:
                try:
                    os.mkdir(part, dir_fd=fd)
                except FileExistsError:
                    pass
            # O_NOFOLLOW makes a symlinked component fail here, on the same
            # descriptor chain the later read or create uses.
            child = os.open(part, _DIR_FLAGS, dir_fd=fd)
            os.close(fd)
            fd = child
    except BaseException:
        os.close(fd)
        raise
    return fd, leaf


def _read_template(root_fd, template):
    parent, leaf = _open_parent(root_fd, template, create=False)
    try:
        # O_NONBLOCK: a FIFO planted at the template name must not hang the
        # open; the type check below then refuses it before any read.
        fd = os.open(leaf, os.O_RDONLY | os.O_NOFOLLOW | os.O_NONBLOCK, dir_fd=parent)
    finally:
        os.close(parent)
    with os.fdopen(fd, "rb") as handle:
        if not stat.S_ISREG(os.fstat(handle.fileno()).st_mode):
            raise OSError("template is not a regular file")
        return handle.read().decode("utf-8")


def _write_all(fd, data):
    view = memoryview(data)
    while view:
        view = view[os.write(fd, view):]


def _publish(parent, leaf, data):
    """Write data under a private temporary name, then link it to leaf.

    Return False if leaf appeared meanwhile; it is then left as it is.
    """
    # Unpredictable and created exclusively, so no other run writes to, removes
    # or publishes this file, and this run removes only the file it created.
    temporary = f".{leaf}.{os.getpid()}.{secrets.token_hex(8)}.init-tmp"
    fd = os.open(
        temporary, os.O_WRONLY | os.O_CREAT | os.O_EXCL | os.O_NOFOLLOW, 0o644,
        dir_fd=parent,
    )
    try:
        try:
            _write_all(fd, data)
            os.fsync(fd)
        finally:
            os.close(fd)
        # link fails if leaf exists, so nothing is ever replaced.
        try:
            os.link(temporary, leaf, src_dir_fd=parent, dst_dir_fd=parent)
        except FileExistsError:
            return False
        return True
    finally:
        os.unlink(temporary, dir_fd=parent)


def _existing(parent, leaf, destination, kept, errors):
    """Classify an existing entry. Return False if leaf does not exist."""
    try:
        mode = os.stat(leaf, dir_fd=parent, follow_symlinks=False).st_mode
    except FileNotFoundError:
        return False
    if stat.S_ISREG(mode):
        kept.append(destination)
    else:
        errors.append(
            f"{destination} exists but is not a regular file. "
            "Move it aside and run this script again."
        )
    return True


def open_root(root):
    return os.open(root, os.O_RDONLY | getattr(os, "O_DIRECTORY", 0))


def init(root):
    """Create missing instance files. Return (created, kept, errors).

    root is a path or an open directory descriptor, which is left open.
    """
    if not supported():
        return [], [], [_UNSUPPORTED]
    if isinstance(root, int):
        return _init(root)
    try:
        root_fd = open_root(root)
    except OSError as exc:
        return [], [], [f"Could not open instance root: {exc}"]
    try:
        return _init(root_fd)
    finally:
        os.close(root_fd)


def _init(root_fd):
    created, kept, errors = [], [], []
    for template, destination, rewrites in INSTANCE_FILES:
        parent = None
        try:
            parent, leaf = _open_parent(root_fd, destination, create=True)
            if _existing(parent, leaf, destination, kept, errors):
                continue
            text = _read_template(root_fd, template)
            for old, new in rewrites:
                text = text.replace(old, new)
            if not _publish(parent, leaf, text.encode("utf-8")):
                # Another run published it first; judge what is there now.
                if not _existing(parent, leaf, destination, kept, errors):
                    errors.append(f"{destination} appeared and vanished during setup.")
                continue
        except (OSError, UnicodeError) as exc:
            errors.append(f"Could not create {destination} from {template}: {exc}")
            continue
        finally:
            if parent is not None:
                os.close(parent)
        created.append(destination)
    return created, kept, errors


def _same_directory(root_fd, path):
    try:
        held, named = os.fstat(root_fd), os.stat(path)
    except OSError:
        return False
    return (held.st_dev, held.st_ino) == (named.st_dev, named.st_ino)


def main():
    parser = argparse.ArgumentParser(
        description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter
    )
    parser.add_argument("--root", type=Path, default=Path(__file__).resolve().parents[1])
    args = parser.parse_args()

    if not supported():
        print(_UNSUPPORTED, file=sys.stderr)
        return 1
    # Resolve once: a --root given through a link is pinned to its target here.
    root = args.root.resolve()
    try:
        root_fd = open_root(root)
    except OSError as exc:
        print(f"Could not open instance root: {exc}", file=sys.stderr)
        return 1
    try:
        created, kept, errors = init(root_fd)
        # Same descriptor as setup: the skills checked are this instance's.
        skill_errors = verify_at(root_fd)
        if not _same_directory(root_fd, root) or root.resolve() != root:
            errors.append(
                f"{root} was replaced while this script ran. Setup and the "
                "skill check used the directory it named at the start, not the "
                "one there now. Run it again."
            )
    finally:
        os.close(root_fd)

    for name in created:
        print(f"Created {name}")
    for name in kept:
        print(f"Kept existing {name}")
    for error in errors:
        print(error, file=sys.stderr)
    for error in skill_errors:
        print(error, file=sys.stderr)
    if skill_errors:
        print("Skill check failed. Do not use the seat until it passes.", file=sys.stderr)
    else:
        print("Installed skills match the lock.")

    if errors:
        print("Instance setup is incomplete.", file=sys.stderr)
    if errors or skill_errors:
        return 1
    if created:
        print("Next: replace the <placeholders> in the created files, "
              "then start the agent from this directory.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
