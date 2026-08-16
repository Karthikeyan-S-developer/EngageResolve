# EngageResolve

> **Real-Time Engagement Conflict Resolution System for AI-Powered Classroom Monitoring**

[![Backend Tests](https://img.shields.io/badge/pytest-22%20passed-success)](file:///backend/tests)
[![Python Version](https://img.shields.io/badge/python-3.11%2B-blue)](https://www.python.org/)
[![Frontend](https://img.shields.io/badge/Expo-React%20Native%20TypeScript-000000)](https://expo.dev/)
[![Database](https://img.shields.io/badge/database-SQLite3-003B57)](https://www.sqlite.org/)
[![License](https://img.shields.io/badge/license-MIT-green)](LICENSE)

---

## 📌 Problem Overview

In AI-powered classroom monitoring, multiple optical cameras (front, side, rear, overhead) continuously emit engagement observations for students. However, camera signals frequently arrive **asynchronously**, **out of order**, **duplicated**, or **in direct conflict** with each other.

For example, `cam-01` might report a student engagement score of `0.90` (with 95% confidence), while `cam-02` simultaneously reports `0.40` (with 60% confidence).

**EngageResolve** is a deterministic real-time reconciliation engine that ingests raw camera signals, resolves conflicting observations, re-orders late out-of-order events, matches student identities across cameras, reconstructs versioned student timelines, and provides human-readable decision traces and side-effect-free replay verification hashes.

---

## ⚡ Core Architecture

EngageResolve transforms raw camera JSON payloads:

```json
{
  "camera_id": "cam-01",
  "timestamp": "2024-06-01T10:00:00Z",
  "student_id": "student-123",
  "engagement_score": 0.75,
  "confidence": 0.90,
  "source": "front_camera"
}
```

Through a strict deterministic 6-step pipeline:

```
Raw Camera Event 
  ➔ 1. Validation 
  ➔ 2. SHA-256 Deduplication 
  ➔ 3. Spatio-Temporal Identity Resolution 
  ➔ 4. Chronological Re-ordering 
  ➔ 5. 6-Tier Conflict Resolution 
  ➔ 6. Reconstructed State Timeline & Human Audit Trace
```

---

## 🛠 Tech Stack

- **Backend**: Python 3.11+, Flask REST API, SQLite (WAL mode with normalized tables & indexes), `pytest`.
- **Frontend**: React Native, Expo, TypeScript, SVG time-series visualizer.
- **Analytics & Exports**: Power BI-compatible CSV dataset exports.
- **Rules Engine**: 100% deterministic rule-based processing (Zero ML/LLM/Cloud API dependencies).

---

## 🎯 Key Features & Algorithms

### 1. 6-Tier Deterministic Conflict Resolution Hierarchy
1. **Rule 1 (Validity)**: Rejects malformed payload values ($0 \le \text{score} \le 1$, valid ISO timestamp).
2. **Rule 2 (Deduplication)**: Ignores duplicate SHA-256 fingerprints idempotently.
3. **Rule 3 (Confidence)**: Higher confidence score wins (e.g. 0.95 vs 0.60).
4. **Rule 4 (Timestamp)**: Earlier timestamp wins if confidence is tied.
5. **Rule 5 (Camera Reliability)**: Higher sensor trust score wins (`front_camera`: 0.95, `side_camera`: 0.85, `rear_camera`: 0.80).
6. **Rule 6 (Stable Fingerprint Tie-breaker)**: Lexicographically smaller SHA-256 fingerprint string.

### 2. Spatio-Temporal Identity Resolution
Calculates a combined match score against recent observations:
$$\text{temporal\_score} = 1 - \min\left(\frac{\Delta t}{5.0\text{s}}, 1.0\right)$$
$$\text{spatial\_score} = 1 - \min\left(\frac{\text{distance}}{100\text{m}}, 1.0\right)$$
$$\text{combined\_score} = 0.6 \cdot \text{temporal\_score} + 0.4 \cdot \text{spatial\_score}$$
If $\text{combined\_score} \ge 0.70$, maps raw camera identifier to canonical student record.

### 3. State Reconstruction & Out-of-Order Handling
Late-arriving events trigger automatic timeline re-ordering. Re-evaluates sequential version numbers ($v_1, v_2, v_3 \dots$) and logs an `OUT_OF_ORDER_EVENT` audit trace detailing affected versions.

### 4. Side-Effect-Free Replay Engine
Re-executes historical event ranges inside an in-memory isolated SQLite sandbox. Produces a canonical SHA-256 result hash that proves **100% determinism** across multiple runs without mutating production database tables.

---

## 🚀 Quick Start & One-Command Launcher

### Prerequisites
- Python 3.11+
- Node.js 18+ and `npm`

### 1. Run Backend Server & Seed Data
```bash
cd backend
python -m venv .venv
# On Windows: .venv\Scripts\activate | On Unix: source .venv/bin/activate
pip install -r requirements.txt
python run.py --seed
```
Backend will start at: `http://localhost:5000`

### 2. Run Frontend Dashboard
```bash
cd frontend
npm install
npm run web
```
Frontend web application will start at: `http://localhost:8081`

### 3. One-Command Developer Launcher Scripts
- **Windows**: `scripts\start-dev.bat`
- **Unix/macOS**: `./scripts/start-dev.sh`

---

## 🧪 Testing & Verification

Run the comprehensive automated `pytest` suite:

```bash
cd backend
python -m pytest tests -v
```

### Test Coverage Highlights
- `test_ingestion.py`: Payload validation & constraint checks.
- `test_duplicates.py`: Event idempotency verification.
- `test_out_of_order.py`: Late event insertion & timeline version re-ordering.
- `test_conflicts.py`: Full 6-tier conflict resolution algorithm tests.
- `test_identity.py`: Spatio-temporal identity mapping & separation.
- `test_replay.py`: Side-effect-free replay sandbox & result hash reproducibility.
- `test_determinism.py`: System-wide state hash determinism.
- `test_performance.py`: Benchmark (~100 events/sec local processing throughput).
- `test_api.py`: End-to-end Flask REST API integration testing.

---

## 📊 Power BI Integration

EngageResolve exports clean CSV datasets directly compatible with Power BI:

- **Engagement Timeline CSV**: `GET /export/engagement.csv`
- **Audit Log CSV**: `GET /export/audit.csv`

Refer to [`docs/powerbi.md`](docs/powerbi.md) for step-by-step visual setup instructions.

---

## 📖 Comprehensive Documentation

- [Architecture Diagram & Specification](docs/architecture.md)
- [Conflict Resolution Algorithm](docs/conflict-resolution.md)
- [Replay Engine & Determinism Verification](docs/replay.md)
- [Identity Resolution Engine](docs/identity-resolution.md)
- [Auditability & Human Traces](docs/auditability.md)
- [REST API Specification](docs/api.md)
- [Live Demonstration Script (5-10 Mins)](docs/demo-script.md)
- [Power BI Integration Guide](docs/powerbi.md)

---

## 📄 License
This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
