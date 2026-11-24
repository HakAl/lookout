# Lookout 1.2.0

Setup can now prepare an instance for Claude Code, and the README says which
agents pick the kit up by themselves and what that statement rests on. The
review skills, the lock, the skill check and the seat's standing instructions
are unchanged.

## What changed

- `scripts/init_instance.py --claude` creates `.claude/skills` as a relative
  link to `.agents/skills`, the location Claude Code documents for project
  skills. The link is created only after the skill check passes. In that
  mode, and also after the skill check passes, setup checks the type and
  target of an existing `.claude/skills`: it is kept if it is exactly that
  link, and anything else is reported as an error and left alone. Without the
  flag, setup creates the same instance files and runs the same skill check
  as in 1.1.0.
- The README has a table for Codex, Antigravity CLI, OpenCode and Claude Code
  with the basis of each row, a fallback prompt for launchers that skip
  project discovery, how to invoke the explicit-only `lookout-skill-audit`,
  and a startup diagnostic.
- `docs/workspace.md` lists `.claude/skills` as an optional instance entry.

## Upgrade

Pull the new kit files. To add the Claude Code link to an existing instance,
run `python3 scripts/init_instance.py --claude`; existing instance files are
kept. Start a new Claude Code session afterwards.

## Known limits

- The agent table rests on one session per agent and setup, on one macOS
  machine. The entries for Antigravity CLI, OpenCode and Claude Code are the
  agents' own startup answers. The Codex entry follows its documentation and
  earlier use as a seat; Codex was not run in a fresh instance for this
  release.
- The Claude Code link is a symbolic link, so it needs a file system and
  platform that support them. The setup script still needs Linux, macOS or
  another Unix, and with or without the flag it now also requires the
  platform to create and read symbolic links relative to an open directory.
- The standalone skill check examines `.agents/skills` and skips
  `.claude/skills`. A link replaced after setup is flagged only by running
  setup with `--claude` again.
- The known limits of 1.1.0 still apply.

## Verification

- Unit tests: 42 passed with Python 3.14.7 on macOS. Not run on Python 3.9 or
  any other version, and not run on Linux. The changed Python files parse with
  the Python 3.9 grammar.
- Fresh-clone checks: the test command passed in a fresh clone of `42bafb5`
  with an empty home directory. That commit contains all code changes in this
  release. The release commit adds this note and README wording.
- Live validation, one initial session per agent plus a new Claude Code
  session after linking: fresh clones of 1.1.0 were set up with the script
  and started under Antigravity CLI 1.5.16, OpenCode 2.3.2 and Claude Code
  2.1.331. Each was asked what it had loaded and given one small review of a
  prepared branch. In the Claude Code instance a prerelease setup script was
  then run with `--claude`: it created the link, a second run kept it, the
  skill check passed, a new session reported eight skills, and
  `/lookout-skill-audit` loaded the audit skill. The released script creates
  the link after the skill check; the prerelease one created it before. Codex
  was not part of this run.
- The public file set matches its explicit allowlist. Private development
  history, raw evidence, transcripts and captures are excluded.
