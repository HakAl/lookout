# Review: <task ID and target>

## Findings and decision

Lead with material findings or “No material findings in the reviewed scope.”
For each finding give severity, location, concrete discrepancy/trigger,
consequence, supporting evidence, and proposed action. Name assumptions that
limit the claim. Keep optional suggestions separate; merge duplicate causes.

## Review receipt

- Target: repository/artifact, exact revision or captured dirty-state identity.
- Request: intended decision, requirements, included and excluded scope.
- Delivery: whether the requested outcome is met; material scope additions or
  system-contract gaps. For implementation evidence, what plausible failure the
  checks distinguish and which claimed integration remains unverified.
- Coverage: questions actually checked; partial and unavailable areas.
- Evidence: source locations and supplied receipts, identified as supplied.
- Verification performed: command, cwd, target/environment, observed result,
  exit code, and log location when useful; say when no execution occurred.
- For acceptance checks: expected condition, actual observed value (also on pass),
  target/run identity and a negative control or stated reason it was unnecessary.
- Provenance: actual reviewers, selected skill revisions when known, assignment
  IDs where applicable; do not invent unavailable identities.
- Limits and next action: remaining uncertainty, responsible owner, and the
  specific evidence or decision needed to resolve it.

Short reviews can collapse this into a paragraph. If a machine-readable report
is requested, use the selected skill's actual schema rather than inventing an
incompatible record. Report completion and findings severity are separate.
