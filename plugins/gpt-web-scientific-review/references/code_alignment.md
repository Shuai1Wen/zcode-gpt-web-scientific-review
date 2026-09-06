# Code–Method Alignment Review Profile

Check that implementation facts match the paper/specification.

## Data

- actual inclusion/exclusion criteria;
- unit of splitting;
- feature construction;
- normalization;
- target construction;
- missing-data handling.

## Model

- tensor shapes correspond to equations;
- response/context variables enter at the claimed layer;
- loss terms and weights match definitions;
- train/eval behavior is aligned;
- stochastic components are controlled where scientifically relevant.

## Evaluation

- metric implementation matches formula;
- baseline receives the same information budget;
- no post-hoc use of test labels;
- no accidental same-subject leakage through caches, aggregates, embeddings, or preprocessing.

Implementation correctness is necessary but not sufficient for scientific validity.
