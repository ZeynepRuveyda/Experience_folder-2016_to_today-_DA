from pathlib import Path
import json

BASE = Path(__file__).parent
jsonl_paths = [BASE/'production_logs.jsonl', BASE/'image_qc.jsonl']

try:
    from pymongo import MongoClient
    HAVE_MONGO = True
except Exception:
    HAVE_MONGO = False

if HAVE_MONGO:
    client = MongoClient('mongodb://localhost:27017')
    db = client['automi_ai']
    for p in jsonl_paths:
        coll = db[p.stem]
        coll.delete_many({})
        with p.open() as f:
            batch = [json.loads(line) for line in f]
            if batch:
                coll.insert_many(batch)
        print('✅ Ingested into Mongo:', p.stem, len(batch))
else:
    # Fallback: keep JSONL as the persisted store
    print('ℹ️ Mongo not available. JSONL fallback in place:')
    for p in jsonl_paths:
        print(' -', p)
