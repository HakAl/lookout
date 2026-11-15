# Review tools

Choose guidance for the artifact and decision. Read the selected skill before
using it. Use explicit local paths so a global skill with a similar name cannot
silently select a different revision.

## Local review skills

| Need | Skill | Boundary |
| --- | --- | --- |
| General code, document, plan or UX review | [lookout-review](.agents/skills/lookout-review/SKILL.md) | Pinned reviewerest snapshot; findings and evidence, no fixes or publication |
| Requirements, plans and operational documents | [lookout-ce-doc-review](.agents/skills/lookout-ce-doc-review/SKILL.md) | CE-derived coherence, feasibility and scope questions; no CE orchestration |
| Rust-specific semantics and failure paths in a change | [lookout-rust-review](.agents/skills/lookout-rust-review/SKILL.md) | Contract-driven supplement; numeric/serialization fidelity, ownership, async behavior and work growth; no automatic optimization or execution |
| Wire formats, SDKs, receipts and persisted records | [lookout-contract-review](.agents/skills/lookout-contract-review/SKILL.md) | Representation, identity and real-reader compatibility; resolve normative contract versus frozen implementation |
| Policy-controlled operations and sandbox boundaries | [lookout-enforcement-review](.agents/skills/lookout-enforcement-review/SKILL.md) | Authority bound to actual effects; receipt ordering, races and truthful outcomes |
| Evaluation plans, pipelines and result claims | [lookout-evaluation-review](.agents/skills/lookout-evaluation-review/SKILL.md) | Units, splits, leakage, metrics, independent evidence and provenance; no experiment authorization |
| Dispatch, acknowledgment, event wakes and recovery | [lookout-recovery-review](.agents/skills/lookout-recovery-review/SKILL.md) | Durable transitions, retries, ownership and uncertain outcomes; no live recovery actions |
| Dependency direction and producer-consumer contracts | [lookout-architecture-review](.agents/skills/lookout-architecture-review/SKILL.md) | Event4u-derived boundary review; stays within the supplied diff |
| Review a skill for quality, dependencies and authority | [lookout-skill-audit](.agents/skills/lookout-skill-audit/SKILL.md) | Open-skills-derived audit; explicit invocation only; returns findings |

General review already covers many concerns. Load a specialist only when its
additional questions improve the decision; do not run the whole table by default.
See [skill admission and updates](docs/skills.md) for provenance and limits.
The [domain selection guide](docs/domain-review-guide.md) maps these supplements
to recurring work.

## Instance tools

Workers, external skills, reference catalogs, inference routes and local
proposals belong to the instance, not the kit. When `TOOLS.local.md` exists
(instance file, created from `templates/TOOLS.local.md`), read it alongside this
table. Sources listed there are not part of the reviewed local install: read and
record their current identity when one is explicitly selected.
