# Biological Validity Review Profile

## Biological unit

State the biological unit explicitly: cell, cell state, donor, clone, tissue, perturbation, disease stage, spatial niche, or longitudinal subject.

## Context-to-target logic

For virtual-cell/virtual-donor work, the reviewer must check whether the observed context actually contains information about the missing state and whether the model transports/conditions that information rather than re-guessing the response from generic embeddings.

## Cross-dataset validity

Before treating one cohort as external validation, check:

- tissue/source;
- assay modality and preprocessing;
- cell composition;
- age/sex/disease inclusion;
- gene/protein feature space;
- intervention vs observation;
- donor-level vs cell-level target.

A negative or positive result is interpretable only if the biological object is commensurate.

## Claim boundaries

Transcriptomic association alone usually does not establish a causal mechanism. Separate:

- predictive validity;
- state reconstruction;
- mechanistic consistency;
- causal intervention evidence.
