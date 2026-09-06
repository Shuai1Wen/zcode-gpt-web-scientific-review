# Experimental Design Review Profile

## Core-first hierarchy

Classify every experiment:

- CORE — directly falsifies the claimed capability;
- SUPPORTING — helps interpret or localize the effect;
- ROBUSTNESS — tests sensitivity/stability;
- ENGINEERING — verifies implementation/reproducibility.

A paper with twenty robustness tests can still lack one necessary core experiment.

## Split design

Match the split to the claim. Examples:

- unseen donor claim -> donor-disjoint split;
- unseen perturbation claim -> perturbation-disjoint split;
- cross-world agent claim -> environment/world holdout;
- temporal forecasting -> future time holdout.

## Paired evaluation

When comparing models, use the same held-out worlds/subjects and budgets whenever possible. Prefer paired uncertainty estimates over unrelated aggregate scores.

## Negative results

A failed validation is evidence. Do not hide it behind additional diagnostics. Use it to decide whether the mechanism, data match, or claim must change.
