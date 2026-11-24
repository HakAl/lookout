# Lookout 1.1.0

Setting up an instance is now one command, and the README is written for
someone seeing the kit for the first time. The review skills, the lock and the
seat's standing instructions are unchanged.

## What changed

- `scripts/init_instance.py` creates `TEAM.md`, `QUEUE.md`, `TOOLS.local.md`
  and `projects/INDEX.md` from `templates/`, adjusts the relative links the
  move would break, and runs the skill check. It never replaces an existing
  entry, and exits 1 if an instance path exists but is not a regular file.
  When it reads templates and creates instance files it does not follow
  symbolic links beneath the instance root. Setup and the skill check use the
  same root directory.
- `scripts/verify_skills.py` gains `verify_at`, used by the setup script. The
  command itself behaves as before.
- The README opens with a plain description, says what Codex and Claude Code
  each pick up by themselves, has a quick start, and describes what a report
  contains. The workspace table moved to `docs/workspace.md`.
- The hand-copy notes in `templates/TEAM.md` and `templates/TOOLS.local.md`
  name the script.

## Upgrade

Pull the new kit files. Existing instance files are not touched, and running
`python3 scripts/init_instance.py` in an existing instance creates only what
is missing.

## Known limits

- The setup script needs Linux, macOS or another Unix. Elsewhere it creates
  nothing and says to copy the templates by hand.
- The script does not fill in placeholders.
- A temporary file left behind by a killed run is not cleaned up by later
  runs. It is a dot file ending in `.init-tmp`.
- The setup script guards the identity of the instance root. It does not
  guard against changes made inside the instance while it runs.
- Skill discovery depends on the agent. The README guidance for Codex and
  Claude Code follows their documentation; see Verification for what was run.
- The integrity check proves the installed skill files match the lock. It does
  not prove a skill is safe or effective.

## Verification

- Unit tests: 34 passed with Python 3.14.7 on macOS. Not run on Python 3.9 or
  any other version, and not run on Linux. The changed Python files parse with
  the Python 3.9 grammar.
- Fresh-clone checks: the test command passed in a fresh clone of commit
  `e666496`, which holds every change in this release except this note, with
  an empty home directory.
- The setup script was run in an existing instance: all four files were kept
  unchanged and the skill check passed.
- Live validation: none. No new instance was created from this release and
  started under any agent.
- The public file set matches its explicit allowlist. Private development
  history, raw evidence, transcripts and captures are excluded.
