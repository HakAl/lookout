# Lookout: a QA team in a box

Lookout is a kit that turns a coding agent into a reviewer for your projects
and agent teams. Ask it to review a branch, a plan or a completion claim, and
it returns supported findings, the verification it actually ran, and a concise
decision for you to act on.

The reviewing agent is called the seat. It works alone by default, and can
dispatch to workers where an instance has provisioned them; `TEAM.md` records
what a given instance actually has.

## Which agents it works with

The kit is plain files: standing instructions in `AGENTS.md` and review skills
in `.agents/skills/`. How much an agent picks up by itself differs:

- **Codex** loads `AGENTS.md` and discovers the skills in `.agents/skills/`
  when started from the instance root with project discovery enabled. The kit
  was developed with a Codex seat.
- **Claude Code** looks for project skills in `.claude/skills/` and reads
  `AGENTS.md` only in some versions and configurations. Confirm it has loaded
  `AGENTS.md`, or tell it to read the file, and give it the path of the skill
  to use, for example `.agents/skills/lookout-review/SKILL.md`.
- **Other agents**: treat them like Claude Code unless their documentation
  says they read both locations.

## Quick start

Requires Python 3.9 or later on Linux, macOS or another Unix.

```sh
git clone https://github.com/HakAl/lookout.git
cd lookout
python3 scripts/init_instance.py
```

The script creates the instance files `TEAM.md`, `QUEUE.md`, `TOOLS.local.md`
and `projects/INDEX.md` from `templates/`, then checks the installed skills
against the lock. It never overwrites an existing file, so it is safe to run
again. Then:

1. Replace the `<placeholders>` in the created files.
2. Start the agent from the instance root and make sure it has the
   instructions and skills, as described for your agent above.

The skill check must pass before the seat is used. To repeat it on its own, run
`python3 scripts/verify_skills.py`.

The default instance is a single seat with no workers. Add workers, a messaging
service such as agent-comms, or other tools afterwards, and record them in
`TEAM.md` and `TOOLS.local.md`. A name typed into a roster is not a verified
registration; confirm it through the service before relying on it.

## Give the seat work

Ordinary requests are enough:

- "Review this branch in `/path/to/repo` against main for release blockers."
- "Check whether this test actually proves the completion claim."
- "Review this plan for missing dependencies and unnecessary scope."
- "Inventory the hygiene hooks across these repositories before we standardize."

Supply a path or artifact, the decision you need to make, and any important scope
or deadline. The seat can fill in the rest from context. For batches, the
[request template](templates/request.md) helps keep assignments self-contained.

## What comes back

A report leads with the findings and the decision. Each finding gives its
severity, location, the concrete discrepancy, the consequence and the evidence
behind it. A review receipt follows: the exact target reviewed, what was and
was not covered, the commands that were run with their observed results, and
the remaining uncertainty. "No material findings" is a valid outcome, and a
short review can be a single paragraph. The
[report template](templates/report.md) has the full shape.

## Workspace

Kit files are shared by every instance and come from this repository:
`AGENTS.md`, `TOOLS.md`, `docs/`, `templates/`, `scripts/`, `.agents/skills/`
and `skills/lock.json`. Instance files belong to one seat, are created from
`templates/` and are never part of the kit; the kit's `.gitignore` keeps them
out of its history. [docs/workspace.md](docs/workspace.md) lists every location
and its purpose.

## Skills and trust

The review skills in `.agents/skills/` were inspected, adapted where necessary
and copied in under `lookout-` names. They have no link to their sources and do
not update themselves. `python3 scripts/verify_skills.py` checks the installed
files against the lock; it detects drift and is not a malware scanner. See
[the skill guide](docs/skills.md) for the set and how a skill is admitted.

## License

Apache License 2.0; see [LICENSE](LICENSE). It covers the original kit
material. [NOTICE](NOTICE) lists the adapted skill packages; those that ship an
upstream license keep it inside their package directory.
