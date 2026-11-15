# Source map

Original local guidance, written for SKILLS-003 on 2026-10-03. No external skill
workflow or implementation was copied.

- [MITRE CWE-367](https://cwe.mitre.org/data/definitions/367.html) describes
  state changing between check and use. Its examples support checking resource
  identity across the operation; they do not establish that any particular
  target is exploitable. Confirm the platform and attacker preconditions.
- Actual OS/runtime API documentation, sandbox implementation and the governing
  effect/receipt contract decide the guarantees. Resolve versions and supported
  environments at review time. This package prescribes no universal syscall,
  permission exception, credential location or fail-closed policy.

Mapping these questions to a particular product plan belongs in the instance's
own records.
Gate ownership and experiment authorization are intentionally not embedded as
permanent facts in this reusable skill.
