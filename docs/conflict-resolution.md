# Deterministic Conflict Resolution Algorithm

EngageResolve uses a strict 6-tier deterministic hierarchy to resolve conflicting engagement signals reported by multiple cameras.

## Decision Hierarchy

```
1. Reject Invalid Event (0.0 <= score/confidence <= 1.0, valid ISO timestamp)
   │
   ▼
2. Ignore Duplicate Fingerprint (SHA-256 canonical hash match)
   │
   ▼
3. Compare Confidence Scores (Higher confidence wins)
   │
   ▼ (Tied confidence)
4. Compare Timestamps (Earlier timestamp wins)
   │
   ▼ (Tied timestamp)
5. Compare Camera Reliability (Higher sensor trust wins: front_camera > side_camera > rear_camera)
   │
   ▼ (Tied reliability)
6. Compare SHA-256 Fingerprints (Lexicographically smaller hash string wins)
   │
   ▼
Commit Deterministic Winner & Generate Human Audit Trace
```

## Worked Example

### Scenario
Two cameras report conflicting observations for `student-104` at overlapping timestamps:

- **Signal A (CAM-01 / front_camera)**:
  - Timestamp: `10:00:00Z`
  - Score: `0.90`
  - Confidence: `0.95`
  - Reliability: `0.95`

- **Signal B (CAM-02 / side_camera)**:
  - Timestamp: `10:00:00Z`
  - Score: `0.40`
  - Confidence: `0.60`
  - Reliability: `0.85`

### Evaluation
1. **Rule 1 (Validity)**: Both events valid.
2. **Rule 2 (Duplicate)**: Fingerprints differ.
3. **Rule 3 (Confidence)**: `0.95 > 0.60`. Signal A wins!

### Audit Explanation Output
```
Why was engagement score 0.90 selected?
• Camera CAM-01 reported score 0.90 with 95% confidence.
• Camera CAM-02 reported score 0.40 with 60% confidence.

Decision Summary: Event evt-cam01 selected because confidence 0.95 exceeded 0.60.
```
