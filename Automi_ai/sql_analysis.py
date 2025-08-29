import duckdb
from pathlib import Path
import pandas as pd

BASE = Path(__file__).parent
agg_path = BASE / 'aggregates.parquet'
prod_path = BASE / 'production_logs.parquet'

con = duckdb.connect()
con.execute("INSTALL parquet; LOAD parquet;")
con.execute(f"CREATE VIEW agg AS SELECT * FROM parquet_scan('{agg_path.as_posix()}')")
con.execute(f"CREATE VIEW prod AS SELECT * FROM parquet_scan('{prod_path.as_posix()}')")

# 1) Daily defect rate
q1 = """
SELECT date,
       SUM(defects) AS defects,
       SUM(items) AS items,
       1.0*SUM(defects)/NULLIF(SUM(items),0) AS defect_rate
FROM agg
GROUP BY 1
ORDER BY 1
"""
daily = con.execute(q1).df()

# 2) Defects by cause
q2 = """
SELECT date, cause, COUNT(*) AS defects
FROM prod
WHERE defect=1 AND cause IS NOT NULL
GROUP BY 1,2
ORDER BY 1,3 DESC
"""
by_cause = con.execute(q2).df()

# 3) Defects by station/team
q3 = """
SELECT date, station, team,
       SUM(defect) AS defects,
       COUNT(*) AS items,
       1.0*SUM(defect)/NULLIF(COUNT(*),0) AS defect_rate
FROM prod
GROUP BY 1,2,3
ORDER BY 1,4 DESC
"""
by_station = con.execute(q3).df()

# 4) Throughput by station
q4 = """
SELECT date, station, COUNT(*) AS items
FROM prod
GROUP BY 1,2
ORDER BY 1,3 DESC
"""
throughput = con.execute(q4).df()

out_dir = BASE / 'powerbi_exports'
out_dir.mkdir(exist_ok=True)

daily.to_csv(out_dir/'daily_defect_rate.csv', index=False)
by_cause.to_csv(out_dir/'defects_by_cause.csv', index=False)
by_station.to_csv(out_dir/'defects_by_station_team.csv', index=False)
throughput.to_csv(out_dir/'throughput_by_station.csv', index=False)

print('✅ Exported CSVs to', out_dir)
