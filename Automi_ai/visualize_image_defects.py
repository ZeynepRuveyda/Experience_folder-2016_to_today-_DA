import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from pathlib import Path
from sklearn.metrics import roc_auc_score

plt.style.use('seaborn-v0_8')
sns.set_palette('Set2')

BASE = Path(__file__).parent
OUT = BASE / 'visuals'
OUT.mkdir(exist_ok=True)

# Load data
prod = pd.read_parquet(BASE/'production_logs.parquet')
img = pd.read_parquet(BASE/'image_qc.parquet')

df = prod.merge(img, on='item_id', how='inner')

# 1) Distribution of image metrics by defect
plt.figure(figsize=(14,5))
for i, col in enumerate(['blur', 'noise', 'brightness'], start=1):
    plt.subplot(1,3,i)
    sns.kdeplot(data=df, x=col, hue='defect', common_norm=False, fill=True, alpha=0.4)
    plt.title(f'{col.capitalize()} by Defect', fontsize=12, fontweight='bold')
    plt.xlabel(col.capitalize())
    plt.ylabel('Density')
plt.tight_layout()
plt.savefig(OUT/'img_feat_density_by_defect.png', dpi=300, bbox_inches='tight')
plt.close()

# 2) Boxplots by defect
plt.figure(figsize=(12,5))
metrics = ['blur','noise','brightness']
long = df[['defect']+metrics].melt(id_vars='defect', var_name='metric', value_name='value')
sns.boxplot(data=long, x='metric', y='value', hue='defect')
plt.title('Image Metrics vs Defect (Boxplot)', fontsize=12, fontweight='bold')
plt.xlabel('Metric')
plt.ylabel('Value')
plt.legend(title='Defect')
plt.tight_layout()
plt.savefig(OUT/'img_feat_box_by_defect.png', dpi=300, bbox_inches='tight')
plt.close()

# 3) Simple separability (AUC) for each metric
auc_rows = []
for col in metrics:
    try:
        auc = roc_auc_score(df['defect'].astype(int), df[col])
    except Exception:
        auc = np.nan
    auc_rows.append({'metric': col, 'AUC': auc})
auc_df = pd.DataFrame(auc_rows)

plt.figure(figsize=(6,4))
sns.barplot(data=auc_df, x='metric', y='AUC', color='#4ECDC4')
plt.ylim(0.5, 1.0)
plt.title('AUC by Image Metric (Defect Prediction)', fontsize=12, fontweight='bold')
for i, v in enumerate(auc_df['AUC']):
    if pd.notna(v):
        plt.text(i, v+0.01, f'{v:.2f}', ha='center', fontweight='bold')
plt.tight_layout()
plt.savefig(OUT/'img_metric_auc.png', dpi=300, bbox_inches='tight')
plt.close()

# 4) Threshold analysis for blur/noise (precision/recall at simple cutoff)
results = []
for col in ['blur','noise']:
    for thr in np.linspace(df[col].quantile(0.2), df[col].quantile(0.8), 7):
        pred = (df[col] >= thr).astype(int)
        tp = int(((pred==1)&(df['defect']==1)).sum())
        fp = int(((pred==1)&(df['defect']==0)).sum())
        fn = int(((pred==0)&(df['defect']==1)).sum())
        precision = tp/(tp+fp) if (tp+fp)>0 else 0
        recall = tp/(tp+fn) if (tp+fn)>0 else 0
        results.append({'metric': col, 'threshold': thr, 'precision': precision, 'recall': recall})
thr_df = pd.DataFrame(results)

plt.figure(figsize=(10,4))
sns.lineplot(data=thr_df, x='threshold', y='precision', hue='metric', marker='o')
plt.title('Precision vs Threshold (Blur/Noise)', fontsize=12, fontweight='bold')
plt.tight_layout()
plt.savefig(OUT/'precision_vs_threshold.png', dpi=300, bbox_inches='tight')
plt.close()

plt.figure(figsize=(10,4))
sns.lineplot(data=thr_df, x='threshold', y='recall', hue='metric', marker='o')
plt.title('Recall vs Threshold (Blur/Noise)', fontsize=12, fontweight='bold')
plt.tight_layout()
plt.savefig(OUT/'recall_vs_threshold.png', dpi=300, bbox_inches='tight')
plt.close()

# 5) Station/team hotspots (image metrics)
img_hot = (df.groupby(['station','team'], as_index=False)
             .agg(avg_blur=('blur','mean'), avg_noise=('noise','mean'),
                  defect_rate=('defect','mean')))
heat = img_hot.pivot(index='station', columns='team', values='avg_blur').sort_index()
plt.figure(figsize=(8,6))
sns.heatmap(heat, annot=True, fmt='.2f', cmap='YlGnBu')
plt.title('Avg Blur by Station x Team', fontsize=12, fontweight='bold')
plt.tight_layout()
plt.savefig(OUT/'avg_blur_station_team.png', dpi=300, bbox_inches='tight')
plt.close()

print('✅ Image defect visuals created in', OUT)
