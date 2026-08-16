# Auditability and Decision Trace Architecture

## Principles

Every state-altering event processed by EngageResolve generates an immutable, structured audit log. Evaluators can audit:
- Why a particular camera signal was selected over another.
- Which specific tie-breaking rule was triggered.
- How out-of-order late events re-ordered the timeline.

## Audit Decision Types

1. `CONFLICT_RESOLUTION`: Evaluated when two or more overlapping signals compete for the same student.
2. `OUT_OF_ORDER_EVENT`: Triggered when an event arrives with a timestamp prior to the latest state version.
3. `IDENTITY_RESOLUTION`: Triggered when spatio-temporal matching resolves a raw ID to a canonical student.
4. `DUPLICATE_EVENT`: Triggered when an exact SHA-256 event fingerprint is submitted.

## Human-Readable Trace Explanation Example

```json
{
  "decision_type": "CONFLICT_RESOLUTION",
  "final_score": 0.82,
  "human_readable_explanation": "Why was engagement score 0.82 selected?\n• Camera cam-01 reported score 0.82 with 91% confidence.\n• Camera cam-02 reported score 0.42 with 74% confidence.\n\nDecision Summary: Event evt-001 selected because confidence 0.91 exceeded 0.74."
}
```
