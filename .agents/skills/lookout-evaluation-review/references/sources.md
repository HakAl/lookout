# Source map

Original local guidance, written for SKILLS-003 on 2026-10-03. No external skill
workflow or implementation was copied.

- [scikit-learn common pitfalls, data leakage](https://scikit-learn.org/stable/common_pitfalls.html#data-leakage):
  learned preprocessing can leak test information; fitting on training inputs
  and applying the learned transformation to held-out inputs are different steps.
- [scikit-learn cross-validation, grouped and time-series data](https://scikit-learn.org/stable/modules/cross_validation.html):
  related observations and temporal structure require split choices matched to
  the intended generalization. This supports checking experimental units, not
  requiring scikit-learn or one splitter in every project.

Both pages were checked on 2026-10-03. Their live API details can change; consult
documentation matching the target dependency for an API-specific finding.
The rest of this package is claim-driven review guidance, not a statistical
standard, power calculator or authorization to execute an experiment.
