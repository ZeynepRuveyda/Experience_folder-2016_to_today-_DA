# Automi AI – Power BI Setup

## Data (import these CSVs)
- `Automi_ai/powerbi_exports/daily_defect_rate.csv`
- `Automi_ai/powerbi_exports/defects_by_cause.csv`
- `Automi_ai/powerbi_exports/defects_by_station_team.csv`
- `Automi_ai/powerbi_exports/throughput_by_station.csv`

## Model
- Create date table: mark as Date table; relate on `date`.
- Relationships:
  - Date[date] 1—* to each fact `date`
  - Optionally create dimension tables: Station, Team, Cause (Distinct from facts) and relate.

## Recommended Pages/Visuals
1) Daily Quality Overview
   - Line: Daily defect rate
   - Cards: Defects, Items, Defect Rate
   - Slicers: Date, Station, Team
2) Root Cause Analysis
   - Bar: Defects by Cause
   - Decomposition tree: Defects → Station → Team → Cause
   - Matrix: Date x Cause with Defects
3) Station Performance
   - Heatmap (Matrix): Station x Team (Defect Rate with conditional formatting)
   - Line small multiples: Throughput by top stations

## Measures (see `measures_dax.txt`)
- Total Defects, Total Items, Defect Rate, Selected Period Defect Rate, YoY/ WoW, Pareto (% cumulative).

## Performance
- Import mode, disable auto date/time; use Date dimension; hide technical columns.

## Publishing
- Publish to workspace; schedule refresh if source on OneDrive/GitHub; set roles (RLS) by station/team if needed.
