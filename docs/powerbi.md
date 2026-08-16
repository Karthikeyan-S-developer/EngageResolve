# Power BI Integration Guide

EngageResolve provides Power BI-compatible CSV dataset exports directly from its Flask backend API. No external cloud database or proprietary Power BI REST API subscription is required.

## Export Endpoints

- **Engagement Timeline CSV**: `http://localhost:5000/export/engagement.csv`
- **Audit Logs CSV**: `http://localhost:5000/export/audit.csv`

## How to Import into Power BI Desktop

1. Open **Power BI Desktop**.
2. Click **Get Data** $\rightarrow$ **Text/CSV**.
3. Select the downloaded `engagement_timeline.csv` (or enter the URL directly via **Get Data** $\rightarrow$ **Web**).
4. Verify column data types:
   - `timestamp`: Date/Time (ISO 8601 UTC)
   - `engagement_score`: Decimal Number (0.0 to 1.0)
   - `confidence`: Decimal Number (0.0 to 1.0)
   - `state_version`: Whole Number
   - `student_id`: Text
   - `camera_id`: Text
5. Click **Load**.

## Suggested Power BI Visual Layout

1. **Line Chart**:
   - Axis: `timestamp`
   - Values: `Average of engagement_score`
   - Legend: `student_id`
2. **Clustered Column Chart**:
   - Axis: `camera_id`
   - Values: `Count of state_id`
3. **Card Metrics**:
   - `Average of engagement_score`
   - `Count of state_id`
4. **Table View**:
   - Columns: `student_id`, `state_version`, `timestamp`, `engagement_score`, `confidence`, `camera_id`, `state_status`
