# Identity Resolution Engine Specification

## Problem Overview

In a multi-camera classroom environment, different cameras may observe the same student under temporary or raw tracking identifiers (e.g. `cam-01` tracking `student-105`, while `cam-02` tracks `raw-desk-05`).

EngageResolve uses a deterministic spatio-temporal scoring engine to map raw observations to canonical student records without requiring machine learning models.

## Scoring Formula

$$\text{temporal\_score} = 1.0 - \min\left(\frac{\Delta t}{\text{TIME\_WINDOW}}, 1.0\right)$$

$$\text{spatial\_score} = 1.0 - \min\left(\frac{\sqrt{(x_1 - x_2)^2 + (y_1 - y_2)^2}}{\text{MAX\_DISTANCE}}, 1.0\right)$$

$$\text{combined\_score} = 0.6 \cdot \text{temporal\_score} + 0.4 \cdot \text{spatial\_score}$$

## Decision Thresholds

- `TIME_WINDOW`: 5.0 seconds
- `MAX_DISTANCE`: 100 spatial units
- `MATCH_THRESHOLD`: 0.70 (70%)

If $\text{combined\_score} \ge 0.70$, the observation is mapped to the candidate student record. Otherwise, a new canonical student record is established.
