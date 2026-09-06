# Algorithm Design Review Profile

## Novel capability test

A new method should change at least one substantive capability:

- hypothesis class;
- information routing;
- search/inference strategy;
- objective/constraint handling;
- adaptation/generalization mechanism;
- uncertainty/decision semantics.

A new name around standard components is not enough.

## Module necessity

For each module ask:

1. What information does it consume?
2. What representation/decision does it change?
3. Why can the base method not do the same thing?
4. What ablation directly tests this mechanism?

## Baseline discipline

Keep strong simple baselines. A nonlinear proposal does not justify weak baselines. Compare under the same data, split, budget, and information contract.

## Agent systems

For an agent/auto-research contribution, distinguish a true closed-loop policy that changes behavior based on evidence from a fixed workflow that simply runs predetermined stages.
