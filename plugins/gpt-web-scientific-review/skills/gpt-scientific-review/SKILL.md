---
name: gpt-scientific-review
description: Build a blind, publication-oriented scientific review packet and prompt for an external GPT Web reviewer. Use when reviewing research questions, mathematical models, algorithms, biological mechanisms, causal identification, experimental designs, code-method alignment, novelty, or manuscripts while preventing anchoring on ZCode's current conclusion.
when_to_use: Use before the first ChatGPT Web submission and again when constructing an adversarial comparison prompt after the blind response has been frozen.
license: MIT
metadata:
  version: 0.1.2
---

# Scientific Review Packet Builder

## Purpose

Construct enough information for an expert reviewer to independently reproduce the central reasoning, while withholding the current ZCode verdict during the blind phase.

## Step 1 — Identify the review axis

Classify the task into one or more axes:

- `SCIENTIFIC_QUESTION`
- `IDENTIFIABILITY`
- `MATHEMATICAL_MODEL`
- `ALGORITHM_DESIGN`
- `BIOLOGICAL_VALIDITY`
- `EXPERIMENTAL_DESIGN`
- `CODE_METHOD_ALIGNMENT`
- `LITERATURE_NOVELTY`
- `MANUSCRIPT_CLAIMS`
- `ADVERSARIAL_REVIEW`

Use this classification to emphasize the relevant checklist. Do not turn every review into all axes if the task is bounded.

## Step 2 — Build `review_packet.md`

Use this structure:

```markdown
# Review Packet

## 1. Central scientific question
A single precise question.

## 2. Intended contribution
What is claimed to be new/useful, without stating whether ZCode believes it succeeds.

## 3. Data / evidence actually available
Datasets, sample structure, variables, splits, measurements, interventions, missingness, known limitations.

## 4. Formal problem definition
Inputs, outputs, latent variables, assumptions, estimands/objectives, constraints.

## 5. Proposed method
Equations, operators, architecture, optimization, inference/training/deployment procedure.

## 6. Experimental design and observed results
Only observed or proposed facts required for review. Mark proposed experiments as proposed.

## 7. Hard constraints
Publication target, no wet lab, compute, data restrictions, no leakage, unseen-world/subject constraints, etc.

## 8. Questions the reviewer must adjudicate
Numbered, answerable questions.

Main-line rule for this section: every question must be capable of changing the verdict (KEEP / REVISE / RECONSTRUCT / REJECT) or the design of the main method. Do not list audit-style, completeness-style, or engineering questions here — if a question's answer cannot alter the central conclusion, it does not belong in the packet.

## 9. Evidence provenance / uncertainty
What is measured, inferred, assumed, or not yet verified.
```

## Blindness rules

Remove evaluation anchoring, not relevant evidence.

Exclude during Phase A:

- ZCode's preferred method;
- current accept/reject recommendation;
- previous reviewers' verdicts;
- rhetorical hints that a method "should" work;
- user preference unless it is a genuine hard constraint.

Keep:

- code behavior that materially determines validity;
- real measured results;
- failed experiments;
- data limitations;
- mathematical definitions;
- explicit project constraints.

## Step 3 — Create `prompt_blind.md`

Use the following reviewer contract, adapted to the domain:

```text
You are an independent scientific reviewer. Treat the material below as if you
had not seen any prior reviewer opinion. Do not infer what answer the submitting
team wants.

Your primary task is to decide whether the proposed work actually solves the
stated scientific problem with the available data and formal assumptions.
Do not replace the main scientific question with engineering hygiene,
robustness, logging, calibration, or stability checks. Those may be supporting
issues, but they are not the main contribution unless the stated problem itself
is about them.

For every major criticism, identify the exact failure mechanism and what evidence
would change your conclusion. Do not demand complexity for its own sake, and do
not use a simple linear explanation where the stated relationship requires a
richer model unless linearity is justified as a baseline or approximation.

Main-line discipline for your solution sections (H and I) — this is a hard
requirement:
- Every change in H must act on the central claim's mechanism: the model, the
  identification strategy, the information flow, or the evaluation of the claim
  itself. A change that cannot alter the verdict does not belong in H; omit it
  rather than list it.
- I must contain only experiments that can falsify or decisively support the
  central claim. Bundle nothing else into I.
- Do NOT include audit-grade work anywhere in H or I: code audits, logging,
  testing infrastructure, refactors, seed/variance checks, hyperparameter
  hygiene, documentation, compliance checklists, or "additional ablations for
  completeness" — unless the stated problem itself is about them.
- Keep supporting / robustness / engineering items only inside G, as one short
  list, and only items that materially interpret the core result.
- If you catch yourself listing many peripheral fixes, stop and compress:
  restate the single main-line failure and the smallest set of changes that
  resolves it. H should normally contain 1-4 changes, I 1-3 experiments.
- Your H and I sections are read as THE solution. Anything incapable of
  changing the verdict must be omitted, not appended.

Return the following sections:
A. Actual scientific question
B. Does the proposed method solve that question?
C. Single most serious scientific failure, if any
D. Mathematical/model appropriateness
E. Identifiability from the available data
F. Methodological novelty relative to the stated contribution
G. Evidence hierarchy: core / supporting / robustness / engineering
H. Required changes to the main method
I. Required experiments that directly test the central claim
J. Final verdict: KEEP / REVISE / RECONSTRUCT / REJECT
K. Confidence (0-100) and unresolved uncertainties

When evidence is insufficient, say exactly what is unresolved instead of
manufacturing certainty.
```

Append the review packet after this contract.

## Domain emphasis

### Mathematical model

Check:

1. every symbol is defined and dimensionally/structurally coherent;
2. objective and constraints correspond to the scientific target;
3. latent variables are learnable from observed variables under stated assumptions;
4. nonlinear operators are justified by the relationship, not added cosmetically;
5. training and inference use the same information contract;
6. the model does not hide leakage in context construction;
7. optimization can plausibly recover the intended solution or approximation.

### Algorithm design

Check:

1. what capability is genuinely new;
2. whether the algorithm uses the information claimed to motivate it;
3. whether a complex pipeline is just a workflow around an unchanged base method;
4. whether each module changes the hypothesis class or inference procedure in a meaningful way;
5. whether baselines are fair and strong;
6. whether ablations isolate the novel mechanism rather than decorative components.

### Biological validity

Check:

1. unit of biological variation: cell, state, donor, tissue, perturbation, clone;
2. whether pooling destroys the target biological structure;
3. whether observed context can identify the missing biological response;
4. whether cross-cohort comparisons are commensurate;
5. whether proposed biological claims exceed what transcriptomic/observational data can establish;
6. whether validation tests the same biological object as the main claim.

### Experimental design

Prioritize experiments that can falsify the central claim. Distinguish:

```text
CORE: directly validates the claimed capability
SUPPORTING: helps interpret the capability
ROBUSTNESS: checks sensitivity/stability
ENGINEERING: checks implementation/reproducibility
```

Do not let numerous robustness checks substitute for one missing core test.

### Code-method alignment

Compare implementation to formal specification:

- actual tensors/variables correspond to defined symbols;
- data split matches claimed generalization unit;
- no hidden target information enters feature/context construction;
- losses and evaluation metrics match paper definitions;
- train/eval modes and baselines are comparable;
- implementation shortcuts do not change the scientific claim.

### Literature novelty

Require a contribution matrix rather than generic "few works combine A+B" novelty. Ask:

- nearest task match;
- nearest mathematical/operator match;
- nearest data/setting match;
- what exact region is already occupied;
- what exact capability remains unoccupied;
- whether the proposed method actually delivers that remaining capability.

## Phase B — Challenge prompt

Only after `response_raw.md` is frozen, build a second prompt:

```text
You previously produced a blind review. That review is now frozen.
Below is the submitting agent's current proposal/conclusion.

Do not discard your blind reasoning and start over. Compare the two positions
conflict by conflict. For each conflict state:
1. blind-review position;
2. submitting-agent position;
3. strongest evidence for each;
4. whether the disagreement is core, supporting, robustness, or engineering;
5. which position is better supported, or whether it remains unresolved;
6. exact change required.

Apply the same main-line discipline as your blind review: point 6 must act on
the central claim's mechanism, and audit-grade changes (code hygiene, logging,
seeds, completeness ablations, documentation) are omitted entirely, not listed.

End with an updated verdict and list every place where your view changed after
seeing the other position, with the evidence that caused the change.
```

Append the frozen blind verdict summary and the current ZCode proposal.
