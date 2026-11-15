# Delegation and coordination

A single seat does the review work itself and can skip the dispatch steps on
this page. The briefing and independence rules still apply to any separately
authorized second reviewer it uses. The rest applies when an instance hands
work to other agents (workers) or messages other teams.
`TEAM.md` (instance file) records who the workers are, how work reaches them
and what the operator has authorized.

## How delegated work flows

1. The seat writes a brief and sends it to a worker through the instance's
   dispatch tool. With agent-comms, a messaging and task-tracking service for
   agent teams, that tool is `dispatch_agent`.
2. The tool records the assignment and returns an ID. Keep the ID with the task.
3. The worker replies with its result and the assignment is closed.
4. The seat checks the result against the evidence before relying on it.

Use the dispatch tool for delegated work. Starting a worker by hand, or using a
generic subagent, leaves nothing tracking the assignment. With no dispatch
tool, do the work directly and note that no dispatched worker was available.

## Briefs

A brief names the target revision, the question, exclusions, the directories
the worker may read, the skill path and its accepted hash, the deliverable, the
checks, and when to stop. Send the whole brief in the message or as a file the
tool delivers; a path only the seat can read is not delivery. The request
template helps with intake and does not replace sections the tool requires.

Give each worker its own writable scratch area. Prefer pinned snapshots and
capture uncommitted input explicitly. Include enough surrounding source to test
a finding, and report what the worker could not reach as a coverage limit. A
registered worker may still be unable to read a target, and a skill installed
in the seat is not automatically visible to a worker.

## Independence and tracking

Assign different requests concurrently. For consequential work, give a second
reviewer the original requirements and source, not another reviewer's
conclusions, and resolve disagreements against evidence, not votes. A
verification assignment may run scoped checks; a read-only reviewer returns
findings and asks the seat for the evidence it needs.

Reuse the same key when retrying a task so it is not assigned twice, and keep
the returned IDs. A timeout or blocked run is incomplete coverage: continue
unrelated work and report the missing result.

## Messaging other teams

Message a team whose work is under review only when the operator has authorized
it. Record a standing authorization and its scope in `TEAM.md`. Unless it says
otherwise, it covers review communication, not changes, merges, publication or
experiments. Use the messaging service when the recipient is registered there;
otherwise use only the fallback recorded in `TEAM.md`. Keep messages actionable
and bounded.

Where the messaging service keeps a handoff note and an inbox for the seat,
read both at the start of a session and settle open items before ending it.
