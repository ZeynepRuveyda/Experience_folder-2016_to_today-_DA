## Automi AI – Industrial QC Analytics (Chanel & Peugeot)

Scope
- Data sources: image quality checks (defects), production logs (station, team, shift)
- Storage: MongoDB (fallback JSONL)
- Compute: PySpark (fallback Pandas)
- SQL analytics: DuckDB (embedded)
- Dashboards: Power BI-ready CSV exports (causes, daily defect rates)
- Versioning: Git & DVC scaffolding

Pipeline
1) generate_data.py – synthetic images/production logs
2) pipeline_pyspark.py – PySpark/Pandas aggregations
3) mongo_ingest.py – upsert into MongoDB (or JSONL)
4) sql_analysis.py – DuckDB queries → powerbi_exports/*.csv

Outputs (powerbi_exports)
- daily_defect_rate.csv
- defects_by_cause.csv
- defects_by_station_team.csv
- throughput_by_station.csv

Run (local)
```
source ../data_analysis_env/bin/activate
python Automi_ai/generate_data.py
python Automi_ai/pipeline_pyspark.py
python Automi_ai/mongo_ingest.py
python Automi_ai/sql_analysis.py
```

Notes
- PySpark optional: script falls back to Pandas if Spark not present.
- Mongo optional: falls back to JSONL file.
- Power BI: import CSVs from powerbi_exports.
