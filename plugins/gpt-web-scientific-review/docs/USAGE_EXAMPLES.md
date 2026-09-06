# Usage Examples

## 1. Normal automatic routing

```text
/gpt-review Does the current unseen-donor model actually identify the missing cell-state distribution from the observed donor context? Review the formal objective, context construction, held-out design, and main experiments.
```

Expected behavior: the orchestrator decides Extra High vs Pro from the scientific stakes.

## 2. Force Extra High

```text
/gpt-review-xhigh Check whether Eq. 7 and the implementation use the same conditioning variables and whether any target-derived aggregate leaks into test-time context.
```

Expected behavior: no automatic promotion to Pro and no silent downgrade below Extra High.

## 3. Force Pro

```text
/gpt-review-pro Final pre-submission review: decide whether the proposed nonlinear response operator is mathematically identifiable, genuinely uses observed exact-gene responses, and is novel relative to the nearest methods. Reconstruct the main method if needed.
```

Expected behavior: verified Pro selection, long-run heartbeat, frozen blind result, challenge/adjudication.

## 4. Manuscript review

```text
/gpt-review Review this manuscript's central contribution, mathematical consistency, claim-evidence alignment, and nearest-work novelty. Do not spend the main review on formatting or seed stability.
```

## 5. Biological project review

```text
/gpt-review-pro Determine whether the virtual-donor design can predict withheld cell states for a genuinely unseen donor from limited observed context, without donor leakage. Separate predictive validity from mechanistic biological claims.
```

## 6. Status only

```text
/gpt-review-status
```

No new ChatGPT request should be created.

## 7. Resume after ZCode restart

```text
/gpt-review-resume 20260906_1730_unseen-donor
```

The command reads the persisted phase and continues from there. If `response_raw.md` is already frozen, it must not rerun the blind phase.

## 8. Collect artifacts

```text
/gpt-review-collect 20260906_1730_unseen-donor
```

This creates a human-readable summary from existing files without contacting ChatGPT again.
