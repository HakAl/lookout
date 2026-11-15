# Lookout

A general review seat for a maintainer's projects and agent teams. The seat
turns review requests into supported findings, relevant verification, and a
concise decision for the maintainer. It works as a single seat, and can dispatch
to workers where an instance has provisioned them; `TEAM.md` records what a
given instance actually has.

## Give the seat work

Ordinary requests are enough:

- “Review this branch in `/path/to/repo` against main for release blockers.”
- “Check whether this test actually proves the completion claim.”
- “Review this plan for missing dependencies and unnecessary scope.”
- “Inventory the hygiene hooks across these repositories before we standardize.”

Supply a path or artifact, the decision you need to make, and any important scope
or deadline. The seat can fill in the rest from context. For batches, the
[request template](templates/request.md) helps keep assignments self-contained.

## Workspace

Kit files are shared by every instance. Instance files belong to one seat, are
created from `templates/` and are never part of the kit.

| Location | Kind | Purpose |
| --- | --- | --- |
| [AGENTS.md](AGENTS.md) | Kit | Standing instructions for the seat |
| [TOOLS.md](TOOLS.md) | Kit | Local review skills and when to select them |
| [docs/delegation.md](docs/delegation.md) | Kit | Assignment and coordination rules |
| [docs/skills.md](docs/skills.md) | Kit | Local skills, provenance, review and update process |
| [docs/domain-review-guide.md](docs/domain-review-guide.md) | Kit | Which specialist skill fits which change |
| [docs/verification.md](docs/verification.md) | Kit | Evidence requirements and verification boundaries |
| [docs/retention.md](docs/retention.md) | Kit | Retained evidence, recovery snapshots and cache cleanup rules |
| [docs/review-priorities.md](docs/review-priorities.md) | Kit | Protect scope and system fit; check actual delivery and meaningful tests |
| [projects/README.md](projects/README.md) | Kit | How to keep sourced project context for future reviews |
| [templates/](templates/) | Kit | Request, report and project formats; starting points for instance files |
| [scripts/](scripts/) | Kit | Skill integrity check and its tests |
| `.agents/skills/` | Kit | Reviewed project-local skill copies |
| `skills/lock.json` | Kit | Accepted skill file hashes and provenance |
| `TEAM.md` | Instance | Team shape, provisioning status, grants and local constraints |
| `QUEUE.md` | Instance | Authoritative local task queue |
| `TOOLS.local.md` | Instance | Workers, external skills, catalogs and other local tools |
| `docs/local/` | Instance | Local records that extend the kit docs |
| `projects/INDEX.md`, `projects/<project>.md` | Instance | The seat's project list and context records |
| `tasks/` | Instance | Durable objectives and acceptance criteria |
| `reviews/<task-id>/` | Instance | Create when a review needs durable artifacts |
| `local/` | Instance | Create for disposable inputs, snapshots, and large logs |
| `skills/provenance.local.json` | Instance | Local source paths and admission receipts behind the lock |
| `unverified/` | Instance | Downloaded catalogs, if any; outside active skill discovery |

## Create an instance

1. Clone the kit into the directory the seat will run from.
2. Copy `templates/TEAM.md` to `TEAM.md`, `templates/QUEUE.md` to `QUEUE.md`,
   `templates/TOOLS.local.md` to `TOOLS.local.md` and
   `templates/projects-index.md` to `projects/INDEX.md`. Replace the
   placeholders. The kit's `.gitignore` keeps these out of the kit history.
3. Run `python3 scripts/verify_skills.py`. It must report that the installed
   skills match the lock before the seat is used.
4. Start the agent from the instance root so it reads `AGENTS.md` and discovers
   `.agents/skills/`.

The default instance is a single seat with no workers. Add workers, a messaging
service such as agent-comms, or other tools afterwards, and record them in
`TEAM.md` and `TOOLS.local.md`. A name typed into a roster is not a verified
registration; confirm it through the service before relying on it.

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
