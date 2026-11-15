# Selecting complementary review skills

These supplements are selected by the changed contract and intended
decision. Use general review discipline and usually one or two relevant lenses;
do not run every skill for every request. This guide adds no project gate.
An instance can keep examples from its own recurring work in
`docs/local/domain-examples.md` (instance file).

| Change or claim | Useful supplement | Typical examples |
| --- | --- | --- |
| Wire format, SDK, receipt, content digest or historical record | [Contract](../.agents/skills/lookout-contract-review/SKILL.md) | Detection and receipt consumers; public SDK bindings |
| Policy-controlled operation, sandbox, signed authority or effect observation | [Enforcement](../.agents/skills/lookout-enforcement-review/SKILL.md) | File adapters; worker custody; authority checked at dispatch |
| Dataset, experiment, benchmark or quality claim | [Evaluation](../.agents/skills/lookout-evaluation-review/SKILL.md) | Dataset splits and judges; whether a speed or quality result supports its claim |
| Dispatch, acknowledgment, event wake, retry or damaged state | [Recovery](../.agents/skills/lookout-recovery-review/SKILL.md) | Acknowledgment recovery; wakeups and journals; message settlement |
| Rust language/library semantics | [Rust](../.agents/skills/lookout-rust-review/SKILL.md) | Numeric fidelity, Serde, async cancellation, ownership |
| Responsibility or dependency changes | [Architecture](../.agents/skills/lookout-architecture-review/SKILL.md) | Controller/observer/verifier boundaries; overlapping system responsibilities |
| Requirements, rollout or operational plan | [Document review](../.agents/skills/lookout-ce-doc-review/SKILL.md) | Feasibility, scope, owners and necessary dependencies |

For a blog draft, ordinary clarity/evidence review is usually enough. For setup
and packaging, trace the installed public path and effective configuration using
general review; a separate Python or TypeScript skill is not justified merely by
the file extension. Add a specialist later if a recurring language-specific gap
appears. Evaluation review is for claim-bearing evidence, not every unit test.

Overlaps are intentional at seams. Contract review asks what data means between
components; enforcement asks what authority permits the actual effect; recovery
asks what survives interruption; evaluation asks what the evidence establishes.
Choose architecture when responsibility/dependency direction is the decision;
choose contract when representation, identity or reader compatibility is the
decision. Use both only when both questions materially affect the change.
Consolidate shared causes into one finding rather than counting reviewers or
lenses as independent evidence.

The packages are read-only reviewer guidance. The host separately owns records,
isolated verification and any authorized fixes. They neither change permissions
nor automatically start tests, workers, models or other services.
