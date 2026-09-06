# Scientific Core Review Profile

Use this profile when the main question is whether a project genuinely solves a scientific problem rather than merely demonstrating a technically functioning pipeline.

## Required questions

1. What is the real scientific object: donor, patient, cell state, perturbation, policy regime, decision process, graph, signal, etc.?
2. What must be predicted, inferred, generated, optimized, or explained?
3. What information is available at deployment/evaluation time?
4. What is genuinely unobserved?
5. Which assumption bridges observed context to the unobserved target?
6. Can the proposed data falsify the central claim?
7. Does the evaluation hold out the correct unit of generalization?
8. Does the method use the distinctive information that motivates it?
9. What finding would have real domain meaning if successful?
10. Which requested checks are secondary and cannot substitute for the missing core test?

## Failure patterns

- impressive reconstruction on randomly held-out rows while the scientific claim concerns unseen subjects/worlds;
- a context-aware architecture whose target response is effectively leaked into context;
- a complex agent/workflow whose central inference is still a simple unchanged heuristic;
- external validation on a biologically/statistically different object;
- many robustness checks after the central estimand has not been identified;
- novelty stated as a combination of components rather than a new capability.
