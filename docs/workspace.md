# Workspace

Every file in a Lookout checkout is one of two kinds. Kit files are shared by
every instance and come from the repository. Instance files belong to one seat:
they are created from `templates/` (most of them by
`scripts/init_instance.py`), are ignored by the kit's `.gitignore` and are never
part of the kit.

| Location | Kind | Purpose |
| --- | --- | --- |
| [AGENTS.md](../AGENTS.md) | Kit | Standing instructions for the seat |
| [TOOLS.md](../TOOLS.md) | Kit | Local review skills and when to select them |
| [docs/delegation.md](delegation.md) | Kit | Assignment and coordination rules |
| [docs/skills.md](skills.md) | Kit | Local skills, provenance, review and update process |
| [docs/domain-review-guide.md](domain-review-guide.md) | Kit | Which specialist skill fits which change |
| [docs/verification.md](verification.md) | Kit | Evidence requirements and verification boundaries |
| [docs/retention.md](retention.md) | Kit | Retained evidence, recovery snapshots and cache cleanup rules |
| [docs/review-priorities.md](review-priorities.md) | Kit | Protect scope and system fit; check actual delivery and meaningful tests |
| [projects/README.md](../projects/README.md) | Kit | How to keep sourced project context for future reviews |
| [templates/](../templates/) | Kit | Request, report and project formats; starting points for instance files |
| [scripts/](../scripts/) | Kit | Instance setup, skill integrity check and their tests |
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
| `.claude/skills` | Instance | Optional link to `.agents/skills` for Claude Code, created by `init_instance.py --claude` |
| `unverified/` | Instance | Downloaded catalogs, if any; outside active skill discovery |
