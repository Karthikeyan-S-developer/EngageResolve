# EngageResolve Demonstration Script (5-10 Minutes)

This script provides a step-by-step demonstration walkthrough suitable for college competitions, technical evaluations, and live project demonstrations.

---

## Prerequisites
1. Ensure the Flask backend is running on `http://localhost:5000` (`python run.py --seed`).
2. Ensure the Expo React Native frontend is running on `http://localhost:8081` (`npx expo start --web`).

---

## Step 1: Real-Time Classroom Intelligence Dashboard
- Open the web dashboard homepage (`http://localhost:8081`).
- Point out the KPI cards: Total Students, Events Ingested, Avg Engagement Score, Conflicts Resolved, and Out-of-Order Reordered Events.
- Highlight the **Camera Fleet Reliability** section showing live trust scores (`front_camera`: 95%, `side_camera`: 85%, `rear_camera`: 80%).

---

## Step 2: Student Engagement Roster & Filters
- Click on **Students** in the top navigation bar.
- Demonstrate filtering by status (`HIGH`, `MODERATE`, `LOW`).
- Search for a specific student (`student-001` or `student-006`).

---

## Step 3: Versioned Student Engagement Profile & Chart
- Select **Student 006 (Conflict Heavy)**.
- Show the interactive **Reconstructed Engagement Timeline** SVG chart.
- Hover/click over points to demonstrate versioned state progression ($v_1, v_2, v_3 \dots$).
- Switch to the **Audit & Decision Traces** tab to inspect the human-readable narrative explanations.

---

## Step 4: Multi-Camera Conflict Inspector
- Click on **Conflicts Inspector** in the navigation bar.
- Highlight a multi-camera signal conflict (e.g. `CAM-01` reporting 0.90 score / 95% confidence vs `CAM-02` reporting 0.40 score / 60% confidence).
- Show how the 6-tier deterministic engine selected `CAM-01` because its confidence exceeded `CAM-02`.

---

## Step 5: Side-Effect-Free Replay Simulator
- Click on **Replay Simulator**.
- Click **Start Side-Effect-Free Replay Run**.
- Show the resulting **Deterministic SHA-256 Hash**.
- Run replay a second time and demonstrate that the SHA-256 hash matches 100% identically without altering production database states.

---

## Step 6: Power BI Data Export
- Navigate to **Settings**.
- Click **Export Engagement Timeline CSV** and **Export Audit Log CSV**.
- Show that clean CSV datasets are generated ready for Power BI import.
