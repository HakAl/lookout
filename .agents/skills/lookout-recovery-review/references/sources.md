# Source map

Original local guidance, written for SKILLS-003 on 2026-10-03. No external skill
workflow or implementation was copied. Recurring review questions came from
Lookout's review assignments on dispatch and recovery systems; their findings
are examples, not permanent facts about those projects.

- [RFC 9110, section 9.2.2](https://www.rfc-editor.org/rfc/rfc9110.html#section-9.2.2)
  distinguishes idempotent request semantics and discusses retries when a
  connection fails before a response is read. It defines HTTP behavior, not
  arbitrary bus or filesystem protocols. Check each actual transport's contract.
- Target queue/storage/runtime documentation and source determine delivery,
  atomicity, durability, locking and cancellation guarantees. Match versions,
  deployment topology and failure assumptions during review. This package
  requires no particular broker, database or exactly-once mechanism.

The related enforcement skill focuses on authority at the actual effect boundary;
this skill focuses on lifecycle state and recovery. Consolidate any shared cause
into one finding when both lenses are selected.
