# Evidence and verification

An instance may name a methodological starting point, such as a maintainer's
own verification design reference, in `TOOLS.local.md` (instance file). Keep
engineering applications distinct from claims about what every model will do.

## Review and execution serve different purposes

A reviewer identifies discrepancies, traces failure paths, and requests evidence.
The host performs authorized checks in an appropriate environment and compares
observed results with criteria. An agent's confidence, reasoning trace, agreement
with another agent, or reported completion is not proof of execution.

For each consequential acceptance claim record:

- The target: exact revision, captured dirty bytes, or package hashes.
- The expected condition and how it will be observed.
- The command or procedure actually used, environment and exit/result status.
- The observed value even when the check passes.
- What plausible failure the check distinguishes and what remains untested.

Use target-specific records, fresh fixtures, run identifiers or before/after
measurements when ambient state could satisfy the assertion. A file that already
existed or a fleet-wide count does not prove the current task produced it.

## Independent checks

For consequential work, give a second reviewer the original requirements and raw
evidence. Do not feed it another reviewer's conclusion as an expected answer.
Use a different model family when that adds useful independence. Resolve
disagreements against evidence, not votes.

Keep criteria fixed during a check. Preserve a failing observation; change a
criterion only when the requirement was wrong and record why. Include a negative
control when it tests a meaningful failure mode. Do not manufacture defects,
demand a finding count, or treat a clean report as inherently suspicious.

## Practical limits

Tests prove only the conditions they distinguish. A deterministic check can be
deterministically wrong, incomplete or pointed at the wrong environment. Static
review remains useful for contracts, source paths and judgment-heavy documents;
label it as inspection rather than execution. Do not execute untrusted code just
to turn an inspection into a binary result.

For skill intake, use several separate observations: package inspection, final-byte
hashes, a drift checker with failure controls, and bounded behavior probes. Neither
static safety review nor a passing probe certifies future behavior. Discovery,
runtime permissions, source parity and task correctness are separate claims.
