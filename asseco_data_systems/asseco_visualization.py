import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

plt.style.use('seaborn-v0_8')
sns.set_palette('Set2')
np.random.seed(42)

# Simulated dataset reflecting Asseco experience
num_sites = 55
sites = [f"site_{i:02d}" for i in range(1, num_sites+1)]
categories = ['Electronics', 'Fashion', 'Home', 'Sports', 'Books']

# Web scraping coverage across sites
coverage = pd.DataFrame({
    'site': sites,
    'category': np.random.choice(categories, size=num_sites, p=[0.3, 0.25, 0.2, 0.15, 0.1]),
    'products_scraped': np.random.randint(800, 5000, size=num_sites),
    'success_rate': np.clip(np.random.normal(0.92, 0.05, size=num_sites), 0.6, 0.99),
    'avg_response_ms': np.random.normal(850, 150, size=num_sites).astype(int)
})
coverage['fail_rate'] = 1 - coverage['success_rate']

# Price change time series for a sample of products
days = pd.date_range('2020-01-01', periods=90, freq='D')
products = [f"P{i:04d}" for i in range(1, 31)]

price_data = []
for p in products:
    base = np.random.uniform(20, 200)
    noise = np.random.normal(0, 1.2, size=len(days))
    trend = np.linspace(0, np.random.uniform(-5, 5), len(days))
    series = np.maximum(5, base + trend + noise.cumsum()*0.1)
    promo_days = np.random.choice(range(len(days)), size=5, replace=False)
    series[promo_days] *= np.random.uniform(0.85, 0.95)
    for d, price in zip(days, series):
        price_data.append({'date': d, 'product': p, 'price': price})
prices = pd.DataFrame(price_data)

# ETL / Excel automation KPIs (weekly)
weeks = pd.date_range('2020-01-06', periods=12, freq='W-MON')
etl = pd.DataFrame({
    'week': weeks,
    'excel_manual_hours': np.clip(np.random.normal(14, 2.0, len(weeks)), 8, 18),
    'macro_runtime_min': np.clip(np.random.normal(12, 3.0, len(weeks)), 6, 20),
    'etl_rows_loaded_k': np.random.randint(150, 600, len(weeks))
})
# Simulate automation rollout reducing manual hours
etl['excel_manual_hours'] = etl['excel_manual_hours'].iloc[0] * np.exp(-0.12*np.arange(len(weeks))) + np.random.normal(0, 0.5, len(weeks))

# 1) Scraping coverage by category (bar)
plt.figure(figsize=(18, 12))
plt.subplot(2, 2, 1)
cat_agg = coverage.groupby('category').agg(products=('products_scraped', 'sum'),
                                           success=('success_rate', 'mean')).sort_values('products', ascending=False)
ax = sns.barplot(x=cat_agg.index, y=cat_agg['products'], color='#4ECDC4')
plt.title('Scraping Coverage by Category (Total Products)', fontsize=14, fontweight='bold')
plt.xlabel('Category')
plt.ylabel('Total Products Scraped')
for idx, val in enumerate(cat_agg['products']):
    plt.text(idx, val + max(cat_agg['products']) * 0.01, f'{int(val):,}', ha='center', va='bottom', fontweight='bold')

# 2) Site success vs response time (scatter)
plt.subplot(2, 2, 2)
scatter = plt.scatter(coverage['avg_response_ms'], coverage['success_rate'], 
                      c=coverage['products_scraped'], cmap='viridis', alpha=0.8, s=70)
plt.colorbar(scatter, label='Products Scraped')
plt.title('Success Rate vs Response Time per Site', fontsize=14, fontweight='bold')
plt.xlabel('Avg Response (ms)')
plt.ylabel('Success Rate')
plt.grid(True, alpha=0.3)

# 3) Price index trend (normalized)
plt.subplot(2, 2, 3)
price_index = prices.groupby('date')['price'].mean()
base = price_index.iloc[0]
idx = (price_index / base) * 100
plt.plot(idx.index, idx.values, color='#FF6B6B', linewidth=2.5)
plt.title('Price Index Trend (Average of 30 SKUs)', fontsize=14, fontweight='bold')
plt.xlabel('Date')
plt.ylabel('Index (base=100)')
plt.xticks(rotation=45)
plt.grid(True, alpha=0.3)

# 4) Excel automation impact (line)
plt.subplot(2, 2, 4)
plt.plot(etl['week'], etl['excel_manual_hours'], marker='o', color='#45B7D1', label='Manual Excel Hours (weekly)')
plt.plot(etl['week'], etl['macro_runtime_min']/60, marker='s', color='#96CEB4', label='Macro Runtime (hours)')
plt.title('Automation Impact on Excel Workload', fontsize=14, fontweight='bold')
plt.xlabel('Week')
plt.ylabel('Hours')
plt.legend()
plt.grid(True, alpha=0.3)
plt.xticks(rotation=45)

plt.tight_layout()
plt.savefig('asseco_overview.png', dpi=300, bbox_inches='tight')
plt.show()

# Additional figure: distribution of site success rates
plt.figure(figsize=(10, 6))
sns.histplot(coverage['success_rate'], bins=15, kde=True, color='#A5D8FF')
plt.title('Distribution of Site Success Rates', fontsize=14, fontweight='bold')
plt.xlabel('Success Rate')
plt.ylabel('Site Count')
plt.tight_layout()
plt.savefig('asseco_success_distribution.png', dpi=300, bbox_inches='tight')
plt.show()

print('✅ Asseco visualizations created:')
print(' - asseco_overview.png')
print(' - asseco_success_distribution.png')
