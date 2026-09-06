---
name: gpt-review-adjudicator
description: Adjudicate disagreements between ZCode and a frozen external GPT Web scientific review using evidence rather than model authority. Use after the blind response is frozen, optionally after adversarial comparison, to produce a conflict matrix, accept/reject/modify decisions, core-method revisions, required experiments, and unresolved issues.
when_to_use: Use at the end of a GPT Web scientific-review job; never use it to overwrite or rewrite the frozen raw review.
license: MIT
metadata:
  version: 0.1.2
---

# Evidence-Based Review Adjudicator

## Non-negotiable principle

GPT Web is an external reviewer, not an authority. ZCode's original answer is also not an authority. Resolve claims with the strongest available evidence and explicit assumptions.

## Inputs

Use, when available:

- `review_packet.md`
- original ZCode proposal/claim
- `response_raw.md` (frozen blind review)
- `challenge_raw.md` (optional second phase)
- source code, data summaries, equations, experimental results, and literature evidence relevant to disputed points

Never edit `response_raw.md` or `challenge_raw.md` during adjudication.

## Step 1 — Extract claims, not prose

Break disagreements into atomic adjudicable issues. Typical issue types:

- scientific target mismatch;
- non-identifiability;
- leakage;
- invalid cross-cohort comparability;
- wrong mathematical operator;
- insufficient use of observed context;
- weak novelty;
- evaluation not testing the claimed generalization unit;
- implementation/specification mismatch;
- overclaiming biological/causal meaning;
- robustness/engineering issue that does not alter the central claim.

## Step 2 — Conflict matrix

Create a table with at least:

| Issue | GPT blind position | ZCode position | Evidence for GPT | Evidence for ZCode | Level | Decision |
|---|---|---|---|---|---|---|

`Level` is one of:

```text
CORE
SUPPORTING
ROBUSTNESS
ENGINEERING
```

`Decision` is exactly one of:

```text
ACCEPT_GPT
REJECT_GPT
MODIFY_BOTH
UNRESOLVED
```

## Step 3 — Decision rules

### ACCEPT_GPT

Use when the external reviewer identifies a concrete failure mechanism supported by data/code/math/literature and ZCode's position lacks stronger evidence.

### REJECT_GPT

Use when the critique relies on an incorrect factual premise, ignores supplied evidence, demands an irrelevant objective, or confuses a supporting issue with the main scientific problem.

### MODIFY_BOTH

Use when both positions capture part of the truth or the correct solution requires a third formulation.

### UNRESOLVED

Use when the available evidence cannot discriminate. State the smallest decisive experiment/derivation/data check needed.

## Step 4 — Protect the scientific main line

After adjudicating individual issues, explicitly answer:

1. What is the central scientific problem now?
2. Does the current method still target it?
3. What one or two changes most affect scientific validity?
4. Which requested additions are only robustness or engineering and therefore cannot substitute for core evidence?

Do not allow a long checklist of peripheral checks to obscure a missing central test.

### Main-line gate (hard rule)

Before anything enters the action lists, test every accepted item with one question:

```text
Can resolving this item change the final verdict or the design of the main method?
```

- If yes → it may enter "Core method changes" or "Core experiments".
- If no → it goes to the supporting list at most.
- Audit-grade items (code hygiene, logging, testing infra, refactors, seed/variance checks, hyperparameter hygiene, documentation, completeness ablations, compliance checklists) are dropped from the action lists entirely. At most, record them as one aggregated line under "Dropped as off-main-line" so the pruning is visible.

The user asked for a scientific review, not an audit report: the deliverable is the smallest set of main-line changes that fixes the central problem, not an exhaustive findings list.

## Step 5 — Produce actionable reconstruction

If the verdict requires changes, specify them at the correct level:

### Mathematical/model changes

- revised variables/estimands;
- revised operator/objective/constraints;
- information available at train vs test;
- assumptions required for identification.

### Algorithm changes

- modules that must change;
- how observed context enters the model;
- what is learned vs provided;
- loss/inference changes;
- baselines that must remain fair.

### Core experiments

Prioritize direct falsification of the main capability. A core experiment must be able to make the central claim fail.

### Supporting experiments

Keep them secondary.

## Step 6 — Final adjudication artifact

Write `adjudication.md` with:

```markdown
# Adjudication

## Final verdict
KEEP / REVISE / RECONSTRUCT / REJECT

## Central scientific question
...

## Conflict matrix
...

## Accepted external-review findings
...

## Rejected external-review findings
...

## Modifications that supersede both views
...

## Core method changes
Only items that passed the main-line gate (can change the verdict or the main design).

## Core experiments
Only experiments that can falsify or decisively support the central claim.

## Supporting / robustness / engineering items
Capped to items that materially interpret the core result.

## Dropped as off-main-line
One aggregated line listing audit-grade suggestions that were pruned and why.

## Unresolved questions and decisive evidence needed
...

## Final project main line
...
```

Set the job to `DONE` only after this artifact is complete.
