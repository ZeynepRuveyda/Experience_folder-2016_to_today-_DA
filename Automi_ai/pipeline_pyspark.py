import os
import pandas as pd
from pathlib import Path

# Optional Spark
try:
    from pyspark.sql import SparkSession
    from pyspark.sql import functions as F
    HAVE_SPARK = True
except Exception:
    HAVE_SPARK = False

BASE = Path(__file__).parent
prod_path = BASE / 'production_logs.parquet'
img_path = BASE / 'image_qc.parquet'
agg_path = BASE / 'aggregates.parquet'

if HAVE_SPARK:
    spark = SparkSession.builder.appName('AutomiAI-QC').getOrCreate()
    prod = spark.read.parquet(str(prod_path))
    img = spark.read.parquet(str(img_path))
    df = prod.join(img, on='item_id', how='left')

    agg = df.groupBy('date', 'station', 'team').agg(
        F.count('*').alias('items'),
        F.sum(F.col('defect').cast('int')).alias('defects'),
        F.avg('blur').alias('avg_blur'),
        F.avg('noise').alias('avg_noise'))
    agg = agg.withColumn('defect_rate', F.col('defects')/F.col('items'))
    agg.write.mode('overwrite').parquet(str(agg_path))

    spark.stop()
else:
    prod = pd.read_parquet(prod_path)
    img = pd.read_parquet(img_path)
    df = prod.merge(img, on='item_id', how='left')
    agg = (
        df.groupby(['date', 'station', 'team'], as_index=False)
          .agg(items=('item_id','count'),
               defects=('defect','sum'),
               avg_blur=('blur','mean'),
               avg_noise=('noise','mean'))
    )
    agg['defect_rate'] = agg['defects']/agg['items']
    agg.to_parquet(agg_path, index=False)

print('✅ Aggregates written:', agg_path)
