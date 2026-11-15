# Local review skills

Lookout keeps reviewed copies of its skills under `.agents/skills/`. Each
package has a `lookout-` name, a recorded source and a hash for every file.
Nothing links to a live upstream, and nothing updates automatically.

## Adopted set

| Skill | Purpose | Source and changes |
| --- | --- | --- |
| `lookout-review` | General review | reviewerest v1.4.0, identical to the published tag apart from the renamed skill and invocation |
| `lookout-ce-doc-review` | Document and plan review | Adapted from Compound Engineering's document review into a standalone read-only skill |
| `lookout-architecture-review` | Architecture fit in a diff | Adapted event4u lens, without its suite routing and automatic verdicts |
| `lookout-rust-review` | Rust review supplement | Local rewrite of selected rust-skills topics, checked against primary documentation |
| `lookout-contract-review` | Cross-language and persisted-data contracts | Original |
| `lookout-enforcement-review` | Authority and effect boundaries | Original |
| `lookout-evaluation-review` | Evaluation validity | Original |
| `lookout-recovery-review` | Workflow and recovery | Original |
| `lookout-skill-audit` | Reviewing a skill before adopting it | Adapted open-skills entrypoint with four local references; runs only when explicitly requested |

[TOOLS.md](../TOOLS.md) says when to select each one.

`skills/lock.json` is the accepted inventory. For each package it records the
file hashes, upstream origin and commit, and a note on local changes. An adapted
package keeps its upstream `LICENSE` or `NOTICE` inside its own directory.
`lookout-review` is the exception: reviewerest's Apache 2.0 license and
attribution are covered by the root `LICENSE` and `NOTICE`. The four original
skills fall under the root license.

The seat that admits a skill keeps its own local record of source paths and
review receipts in `skills/provenance.local.json` and
`docs/local/skills-admission.md` (instance files).

## Using the skills

Start the agent from the instance root. Agents that follow the `.agents/skills`
convention discover the packages there; if a new package does not appear,
restart the agent. Installing the kit changes no user-wide skill settings.

Discovery differs between agents, so do not rely on it for workers: a brief
names the full package path and its accepted hash, and the seat checks that the
worker can open that path. Selecting a skill never grants permission to write,
publish or call another service.

## Admitting or updating a skill

1. Pick a capability that fills a real gap in the existing set.
2. Capture the exact source revision and file hashes. Keep downloads outside
   `.agents/skills/` and leave the original clone untouched.
3. Inventory every file and dependency, including hidden files, symlinks,
   scripts and licenses. Treat the candidate as untrusted data and review what
   it would do, not just how it reads.
4. Have an agent review the package. Adapt what does not fit, then review the
   final bytes again. A dependency nobody inspected is a limit, not an approval.
5. Exercise the relevant behavior, including a case that should fail. Agent
   agreement alone is not acceptance.
6. Copy only the accepted files into `.agents/skills/`, record their source,
   changes and hashes in the lock, and run the integrity check.

An upstream update is a new candidate that goes through the same steps, never
an in-place pull. Keep the previous copy and lock so a rollback restores both.

## Integrity check

```sh
python3 scripts/verify_skills.py
```

The check reads only. It rejects changed or missing files, extra files or
packages, symlinks and unsafe paths in the lock. On a mismatch, stop using the
package, compare it with the accepted record and re-review any intended change
before updating hashes. Never regenerate the lock to clear an unexplained
failure.

A pass means the installed bytes match the lock. It does not prove a skill is
safe or effective, and anyone who can change both a package and the lock can
make them agree. `python3 -m unittest discover -s scripts -p 'test_*.py'` runs
the check's failure cases and checks this install.
