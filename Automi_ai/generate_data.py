import json
import random
from datetime import datetime, timedelta
from pathlib import Path
import numpy as np
import pandas as pd

OUT_DIR = Path(__file__).parent
SEED = 42
random.seed(SEED)
np.random.seed(SEED)

# Stations/Teams/Shifts and defect causes
STATIONS = [f"S{i:02d}" for i in range(1, 11)]
TEAMS = ["A", "B", "C"]
SHIFTS = ["Day", "Evening", "Night"]
CAUSES = ["Scratch", "Dust", "ColorMismatch", "Misalignment", "Crack", "Other"]

START = datetime(2022, 1, 1)
DAYS = 120

# Generate production logs (row per item)
rows = []
image_rows = []
item_id = 0
for d in range(DAYS):
    day = START + timedelta(days=d)
    for st in STATIONS:
        base = np.random.poisson(180)  # throughput base per station/day
        for team in TEAMS:
            for shift in SHIFTS:
                n = max(20, int(base * np.random.uniform(0.7, 1.3) / 3))
                for _ in range(n):
                    item_id += 1
                    defect = np.random.choice([0, 1], p=[0.92, 0.08])
                    cause = np.random.choice(CAUSES) if defect else None
                    rows.append({
                        "date": day.date().isoformat(),
                        "station": st,
                        "team": team,
                        "shift": shift,
                        "item_id": item_id,
                        "defect": defect,
                        "cause": cause,
                    })
                    # Image/quality features (simulated)
                    image_rows.append({
                        "item_id": item_id,
                        "blur": float(np.clip(np.random.normal(0.4 if defect else 0.2, 0.1), 0, 1)),
                        "noise": float(np.clip(np.random.normal(0.5 if defect else 0.3, 0.1), 0, 1)),
                        "brightness": float(np.clip(np.random.normal(0.6, 0.15), 0, 1)),
                        "width": int(np.random.choice([1024, 1280, 1600])),
                        "height": int(np.random.choice([768, 960, 1200])),
                    })

prod_df = pd.DataFrame(rows)
img_df = pd.DataFrame(image_rows)

OUT_DIR.mkdir(parents=True, exist_ok=True)
prod_path = OUT_DIR / "production_logs.parquet"
img_path = OUT_DIR / "image_qc.parquet"
prod_df.to_parquet(prod_path, index=False)
img_df.to_parquet(img_path, index=False)

# Also keep JSONL for Mongo fallback
(json_path := OUT_DIR / "production_logs.jsonl").write_text("\n".join(prod_df.to_json(orient="records", lines=True).splitlines()))
(json_img := OUT_DIR / "image_qc.jsonl").write_text("\n".join(img_df.to_json(orient="records", lines=True).splitlines()))

print("✅ Generated:")
print(f" - {prod_path.name} ({len(prod_df):,} rows)")
print(f" - {img_path.name} ({len(img_df):,} rows)")
print(f" - {json_path.name}, {json_img.name} (Mongo fallback)")
