# Rbench Task Samples

Curated RBioBench clinical-track task samples for discussing how benchmark tasks relate to LLM and agent capability boundaries.

This repository is now organized around a vetted shortlist rather than the earlier five-case draft. The previous `derive_vars_dt` first case is intentionally removed from the showcase set because it depends on a run-date fallback and is not useful for discussion.

## Current Shortlist

- 5 `admiral` tasks with clear clinical or ADaM relevance.
- 15 additional `clinical_pilot` tasks from any package.
- Selection goal: prompts should be defensible, failures should reflect model or agent limitations rather than obvious benchmark defects.

See [docs/clinical_shortlist.md](docs/clinical_shortlist.md) for the current candidate list and exclusion criteria.

## Selection Rules

Prefer tasks that test:

- clinical derivation semantics, such as treatment-emergent flags, on-treatment flags, TTE parameters, period datasets, joins, and transposed ADaM structures;
- R-specific execution boundaries, especially tidy-eval, quosures, list-like objects, S3/S4 objects, RDS serialization, and strict CSV schemas;
- package-specific workflows where the prompt and reference code make the expected behavior inspectable.

Exclude tasks that are mainly:

- run-date or current-time fallbacks;
- `summary.csv`-only false failures where the substantive `result.csv` already matches;
- smoke tests, print/list/quote wrappers, or trivial scalar wrappers;
- non-exported function calls unless the prompt explicitly says to use the internal helper or fallback;
- placeholder fixtures that erase the clinical meaning of the task.

## Contributor Hygiene

This repository is intentionally initialized as a clean repository rather than copied from another repo. Commits should use the GitHub noreply identity for `xihaopark`:

```text
xihao park <103370372+xihaopark@users.noreply.github.com>
```
