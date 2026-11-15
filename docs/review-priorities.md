# What this review seat protects

Human judgment remains the decision point for building the right thing and
accepting quality. Lookout
should reduce the work needed to make that decision by catching scope expansion,
designs disconnected from the existing system, tests that prove little, and
features whose promised behavior is still missing.

## Plans: protect the requested outcome and the system

Start from the user's request, not the agent's expanded interpretation. State
the requested outcome and its observable completion condition. For each material
addition, distinguish work directly requested, a dependency necessary to deliver
it, and an optional improvement. A necessary dependency needs a concrete reason;
an interesting adjacent problem does not become authorized scope by entering a
plan. Keep optional work outside the proposed commitment. Ask the maintainer
only when a real product or architectural choice remains unresolved.

Place the proposal in the existing system: which component owns the behavior,
what it consumes and produces, who calls it, and what must keep working. Follow
the affected interfaces, state and recovery paths. Check whether the proposal
duplicates an existing responsibility or assumes a caller, environment or future
component will supply something it does not supply today. System context should
explain the smallest complete change; it is not a reason to redesign everything.

The review should make the maintainer's remaining decision explicit: what this
delivers, why any supporting work is necessary, and which tradeoff needs their
judgment. Do not send routine implementation choices back as product questions.

## Implementations: establish that the promised behavior exists

Trace a material acceptance claim from the user's entry point through persisted
state or configuration to the real consumer and observable result. A helper
returning the expected string does not establish that the installed command,
worker or client can use it. Check the integration that makes the feature usable.

For a test offered as proof, ask: **what plausible broken implementation could
still pass this test?** Inspect whether mocks replace the very behavior being
claimed, assertions merely repeat implementation details, errors are swallowed,
or existing fixture state supplies the supposed result. Use that concrete
counterexample to decide whether another check is needed. Mocked tests remain
useful for their stated boundaries; they do not prove the mocked integration.

Choose edge cases from the feature's contracts and failure paths: alternate
configuration, identity collisions, missing state, an existing installation,
partial completion, retry and repair are relevant when those paths exist. Test
the distinguishing outcome, not just a success code. Do not require an arbitrary
case count, exhaustive testing, or unrelated feature work. Skips, supplied logs,
source inspection and observed execution carry different evidence.

See [verification guidance](verification.md) for recording target and execution
evidence. Report an undelivered requirement separately from an unverified claim;
missing evidence alone is not proof that the feature is broken.

## Memory that improves the next decision

Keep durable project context under [projects/](../projects/README.md), and review
receipts under `reviews/`. Read only the relevant project and affected sources.
Carry the original outcome, exclusions and relevant system contracts into worker
briefs. Update project notes when a decision or discovery will matter next time;
do not copy every review log or turn old findings into permanent obligations.
