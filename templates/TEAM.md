# Lookout team

Instance file. Copy to `TEAM.md` at the instance root and replace every
`<placeholder>`. Record only what has been observed; a name typed here is not a
verified registration. `scripts/init_instance.py` makes the copy and adjusts
the links; in a copy made by hand, remove the `../` prefix from links.

## State

Single seat, set up on <date>. No workers and no messaging service are set up.
The seat does review work directly.

| Actor | Runtime | Intended responsibility | State |
| --- | --- | --- | --- |
| `<seat name>` | <runtime and model> | Intake, scope, review, evidence checks, synthesis | <how identity was checked, or "not checked"> |

Workspace: `<instance root>`.
Versioning and backup: <for example "private Git repository, no remote", or
"not versioned">.

## Delegation

Generic assignment and coordination rules are in
[docs/delegation.md](../docs/delegation.md). This instance does not delegate
yet. When workers or a messaging service such as agent-comms are added, record
here: the actual worker names and directories, how identity and delivery were
checked, and a link to the service's messaging rules. Keep credentials and auth
configuration out of this file.

## Coordination

No standing authorization to message other teams has been granted. Record any
grant here with its date and scope, and name the fallback channel to use for
recipients who are not registered with the messaging service.

## Local constraints

- <constraints of this machine, account or operator, for example which CLI
  tools may be relied on>
- Preserve existing checkouts and uncommitted work. Record exact revisions when
  fetching or preparing review material; remote refs may be stale.
