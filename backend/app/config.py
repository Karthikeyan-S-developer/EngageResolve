import os

class Config:
    # Database
    DB_PATH = os.getenv("DB_PATH", os.path.join(os.path.dirname(os.path.dirname(__file__)), "engageresolve.db"))

    # Identity Resolution Thresholds
    IDENTITY_TIME_WINDOW_SECONDS = float(os.getenv("IDENTITY_TIME_WINDOW_SECONDS", "5.0"))
    IDENTITY_MATCH_THRESHOLD = float(os.getenv("IDENTITY_MATCH_THRESHOLD", "0.70"))
    SPATIAL_MAX_DISTANCE = float(os.getenv("SPATIAL_MAX_DISTANCE", "100.0"))

    # Engagement Classification Thresholds
    HIGH_ENGAGEMENT_THRESHOLD = float(os.getenv("HIGH_ENGAGEMENT_THRESHOLD", "0.75"))
    LOW_ENGAGEMENT_THRESHOLD = float(os.getenv("LOW_ENGAGEMENT_THRESHOLD", "0.45"))

    # Camera Reliability Scores
    CAMERA_RELIABILITY = {
        "front_camera": 0.95,
        "cam-01": 0.95,
        "cam-02": 0.85,
        "cam-03": 0.80,
        "cam-04": 0.75,
        "side_camera": 0.85,
        "rear_camera": 0.80,
        "overhead_camera": 0.90,
    }
    DEFAULT_CAMERA_RELIABILITY = 0.70

    @classmethod
    def get_camera_reliability(cls, camera_id_or_source: str) -> float:
        if not camera_id_or_source:
            return cls.DEFAULT_CAMERA_RELIABILITY
        return cls.CAMERA_RELIABILITY.get(camera_id_or_source.lower(), cls.DEFAULT_CAMERA_RELIABILITY)

    # Anomaly Detection Thresholds
    ANOMALY_SUDDEN_DROP_THRESHOLD = float(os.getenv("ANOMALY_SUDDEN_DROP_THRESHOLD", "0.40"))
    ANOMALY_CONFLICT_WINDOW_SECONDS = float(os.getenv("ANOMALY_CONFLICT_WINDOW_SECONDS", "3.0"))
