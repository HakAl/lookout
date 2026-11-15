# Review evidence retention

Keep review requests/reports, project context, the queue, team/tool guidance,
templates, maintenance scripts, and accepted skill packages together with
their lock. Keep captured dirty sources, source manifests, patches, test
logs, synthetic probes, negative controls, result artifacts and delivery
receipts referenced by those reviews. A directory being under `local/` or
Git-ignored does not make its contents disposable.

Remove build caches only by a named, reviewed path after checking that the
review is complete, no visible process is using the cache, and unique evidence
has been retained outside it. If a receipt identifies an exact executable,
preserve that executable and verify its recorded hash before cleanup. Keep
the original receipt and record the relocation separately.

Recovery snapshots belong under `local/backups/`, with a member inventory,
SHA256 hashes, an archive checksum and an observed restore-verification receipt.
Include root guidance and `.gitignore`, `.agents/`, `docs/`, `projects/`,
`reviews/`, `scripts/`, `skills/`, `tasks/`, `templates/`, and retained `local/`
evidence. Explicitly list cache exclusions. Exclude the snapshot destination
itself. Preserve symlinks as links without traversing their targets.

Any `unverified/` catalog clones remain untouched and outside this
snapshot scope. `.idea/` is editor state. `.agent-comms/`, if present, is
runtime state of the agent-comms messaging service; its database and handoff
notes are backed up by whoever runs that service, not by a workspace archive. Linked
external source repositories and system dependencies are not included merely
because a captured file references them.

A recovery archive on the same disk protects against accidental local deletion;
it does not protect against loss of the disk. Record where off-disk copies are
kept, how each was verified, and what the machine's other backup products do or
do not cover in `docs/local/retention-record.md` (instance file). One verified
snapshot is not an automatic backup schedule.
