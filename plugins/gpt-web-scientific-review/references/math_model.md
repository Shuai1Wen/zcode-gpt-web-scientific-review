# Mathematical Model Review Profile

## Structure audit

For every mathematical object check:

- domain/codomain and dimensions;
- what is observed vs latent;
- dependence structure;
- invariances/equivariances that should hold;
- objective and constraints;
- train-time and test-time information;
- optimization or inference procedure.

## Identification

A formal model is not useful if its key latent quantity cannot be inferred from the observed data under stated assumptions. Require the reviewer to distinguish:

- parameter identifiability;
- predictive identifiability;
- empirical learnability under finite data;
- optimization difficulty.

These are different failure modes.

## Nonlinearity

A nonlinear operator is justified when the scientific relation contains interactions, context-dependent effects, saturation, composition effects, latent mixtures, conditional transport, or other structure not captured by the baseline. Complexity is not evidence of correctness; every added operator must have a role in the information map.

## Leakage

Write an explicit information set for training and deployment. If target-derived statistics, target cells, labels, future outcomes, or same-world aggregates enter deployment features, flag leakage even if the code path looks indirect.
