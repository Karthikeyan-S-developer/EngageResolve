from typing import Dict, Any, List, Optional
from app.config import Config

class ContextRuleEngine:
    CONTEXT_THRESHOLDS = {
        "lecture": {"min_expected": 0.60, "high_threshold": 0.80},
        "group_work": {"min_expected": 0.50, "high_threshold": 0.75},
        "exam": {"min_expected": 0.70, "high_threshold": 0.85},
        "discussion": {"min_expected": 0.55, "high_threshold": 0.75},
    }

    @classmethod
    def evaluate_context(cls, score: float, context_mode: str = "lecture") -> Dict[str, Any]:
        cfg = cls.CONTEXT_THRESHOLDS.get(context_mode.lower(), cls.CONTEXT_THRESHOLDS["lecture"])
        is_below_expected = score < cfg["min_expected"]
        is_above_high = score >= cfg["high_threshold"]
        
        return {
            "context_mode": context_mode,
            "min_expected": cfg["min_expected"],
            "high_threshold": cfg["high_threshold"],
            "is_below_expected": is_below_expected,
            "is_above_high": is_above_high,
            "status": "LOW_FOR_CONTEXT" if is_below_expected else ("HIGH_FOR_CONTEXT" if is_above_high else "EXPECTED")
        }


def detect_state_anomalies(
    current_score: float,
    previous_score: Optional[float],
    competing_events_count: int = 1
) -> List[Dict[str, Any]]:
    """
    Deterministic rule-based anomaly detection for student engagement state changes.
    """
    anomalies = []

    # 1. Sudden engagement drop detection
    if previous_score is not None:
        drop = previous_score - current_score
        if drop >= Config.ANOMALY_SUDDEN_DROP_THRESHOLD:
            anomalies.append({
                "type": "SUDDEN_ENGAGEMENT_DROP",
                "severity": "HIGH",
                "details": f"Engagement score dropped suddenly by {drop:.2f} (from {previous_score:.2f} to {current_score:.2f})."
            })

    # 2. Conflicting multi-camera signal concentration
    if competing_events_count > 2:
        anomalies.append({
            "type": "HIGH_CAMERA_DISCREPANCY",
            "severity": "MEDIUM",
            "details": f"Detected {competing_events_count} competing camera signals in a tight temporal window."
        })

    return anomalies
