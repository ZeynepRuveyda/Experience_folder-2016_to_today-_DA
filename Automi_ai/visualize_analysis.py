import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from pathlib import Path

plt.style.use('seaborn-v0_8')
sns.set_palette('Set2')

BASE = Path(__file__).parent
EXP = BASE / 'powerbi_exports'
OUT = BASE / 'visuals'
OUT.mkdir(exist_ok=True)

# Load CSVs
Daily = pd.read_csv(EXP/'daily_defect_rate.csv', parse_dates=['date'])
ByCause = pd.read_csv(EXP/'defects_by_cause.csv', parse_dates=['date'])
ByStation = pd.read_csv(EXP/'defects_by_station_team.csv', parse_dates=['date'])
Throughput = pd.read_csv(EXP/'throughput_by_station.csv', parse_dates=['date'])

# 1) Daily defect rate trend
plt.figure(figsize=(12,6))
plt.plot(Daily['date'], Daily['defect_rate']*100, color='#FF6B6B', linewidth=2.5)
plt.title('Daily Defect Rate (%)', fontsize=14, fontweight='bold')
plt.xlabel('Date')
plt.ylabel('Defect Rate (%)')
plt.grid(True, alpha=0.3)
plt.tight_layout()
plt.savefig(OUT/'daily_defect_rate.png', dpi=300, bbox_inches='tight')
plt.close()

# 2) Top defect causes (overall)
causes = (ByCause.groupby('cause', as_index=False)['defects']
                 .sum().sort_values('defects', ascending=False).head(10))
plt.figure(figsize=(10,6))
sns.barplot(data=causes, x='defects', y='cause', color='#4ECDC4')
plt.title('Top Defect Causes', fontsize=14, fontweight='bold')
plt.xlabel('Defect Count')
plt.ylabel('Cause')
for i, v in enumerate(causes['defects']):
    plt.text(v, i, f' {int(v)}', va='center', fontweight='bold')
plt.tight_layout()
plt.savefig(OUT/'defects_by_cause_top10.png', dpi=300, bbox_inches='tight')
plt.close()

# 3) Heatmap: defect rate by station vs team (overall)
pivot = (ByStation.groupby(['station','team'], as_index=False)
                   .agg(defects=('defects','sum'), items=('items','sum')))
pivot['defect_rate'] = pivot['defects']/pivot['items']
heat = pivot.pivot(index='station', columns='team', values='defect_rate').sort_index()
plt.figure(figsize=(8,6))
sns.heatmap(heat*100, annot=True, fmt='.1f', cmap='YlOrRd')
plt.title('Defect Rate by Station x Team (%)', fontsize=14, fontweight='bold')
plt.xlabel('Team')
plt.ylabel('Station')
plt.tight_layout()
plt.savefig(OUT/'defect_rate_station_team_heatmap.png', dpi=300, bbox_inches='tight')
plt.close()

# 4) Throughput trend for top stations
top_stations = (Throughput.groupby('station')['items'].sum()
                           .sort_values(ascending=False).head(5).index.tolist())
sel = Throughput[Throughput['station'].isin(top_stations)]
plt.figure(figsize=(12,6))
for st in top_stations:
    sub = sel[sel['station']==st]
    plt.plot(sub['date'], sub['items'], label=st, linewidth=2)
plt.title('Throughput Trend (Top 5 Stations)', fontsize=14, fontweight='bold')
plt.xlabel('Date')
plt.ylabel('Items per Day')
plt.legend(title='Station')
plt.grid(True, alpha=0.3)
plt.tight_layout()
plt.savefig(OUT/'throughput_trend_top5.png', dpi=300, bbox_inches='tight')
plt.close()

print('✅ Visuals created in', OUT)
