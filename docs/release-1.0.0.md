# Lookout 1.0.0

First public release. Lookout is a kit for running a review seat: an agent that
turns review requests into supported findings and a clear decision for the
maintainer.

## What is in it

- Standing instructions for the seat (`AGENTS.md`) and guidance on review
  priorities, verification, delegation and evidence retention (`docs/`).
- Nine review skills under `.agents/skills/`, each with a `lookout-` name:
  general review, document review, architecture, Rust, contracts, enforcement,
  evaluation, recovery, and skill audit.
- `skills/lock.json`, which records a hash for every skill file, and
  `scripts/verify_skills.py`, which checks the installed files against it.
- Templates for the files each instance creates for itself: team, queue, local
  tools and project index.

## Getting started

Follow "Create an instance" in the README. The default instance is a single
seat with no workers.

## Known limits

- Setting up an instance is a manual copy of four templates. There is no
  bootstrap script yet.
- The integrity check proves the installed skill files match the lock. It does
  not prove a skill is safe or effective.
- Skill discovery depends on the agent. One that does not read
  `.agents/skills` needs the skill paths given to it explicitly.

## Verification

- Unit tests: 10 passed with Python 3.14.7. Not run on other Python versions.
- Fresh-clone checks: the test command passed in a fresh clone of the release
  commit with an empty home directory.
- A deliberately corrupted skill file makes both the integrity check and the
  test command fail.
- Live validation: none. No new instance was started from this release.
- The public file set matches its explicit allowlist. Private development
  history, raw evidence, transcripts and captures are excluded.
