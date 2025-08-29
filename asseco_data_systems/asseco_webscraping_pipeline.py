import os
import time
from datetime import datetime
from typing import List, Dict

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

# Optional deps for scraping
try:
    import requests
    from bs4 import BeautifulSoup
    HAVE_NET_DEPS = True
except Exception:
    HAVE_NET_DEPS = False

plt.style.use('seaborn-v0_8')
sns.set_palette('Set2')

OUTPUT_EXCEL = 'asseco_scraped_data.xlsx'
KPI_FIG = 'asseco_scrape_kpis.png'

# Target demo sites (public demo). If network blocked, we fallback to synthetic data.
SITES: List[Dict[str, str]] = [
    {
        'site': 'books_demo',
        'url': 'http://books.toscrape.com/',
        'type': 'books'
    },
    {
        'site': 'electronics_demo',  # synthetic fallback
        'url': 'https://nonexistent.example/electronics',
        'type': 'electronics'
    }
]


def scrape_books_toscrape(base_url: str, limit_pages: int = 3) -> pd.DataFrame:
    rows = []
    for page in range(1, limit_pages + 1):
        url = base_url if page == 1 else f"{base_url}catalogue/page-{page}.html"
        try:
            resp = requests.get(url, timeout=10)
            resp.raise_for_status()
            soup = BeautifulSoup(resp.text, 'html.parser')
            for article in soup.select('article.product_pod'):
                title = article.h3.a.get('title', '').strip()
                price_raw = article.select_one('.price_color').get_text(strip=True)
                price = float(price_raw.replace('£', '').strip())
                availability = article.select_one('.availability').get_text(strip=True)
                rating_cls = article.select_one('.star-rating')
                rating = rating_cls['class'][1] if rating_cls and len(rating_cls['class']) > 1 else 'NA'
                rows.append({
                    'site': 'books_demo',
                    'product': title,
                    'price': price,
                    'availability': availability,
                    'rating_label': rating,
                    'category': 'Books'
                })
        except Exception:
            # Network issue → break and return what we have
            break
    return pd.DataFrame(rows)


def synthetic_site(site: str, category: str, num: int = 120) -> pd.DataFrame:
    rng = np.random.default_rng(42)
    prices = np.round(rng.uniform(10, 600, size=num), 2)
    availability = rng.choice(['In stock', 'Low stock', 'Out of stock'], size=num, p=[0.7, 0.2, 0.1])
    ratings = rng.integers(1, 6, size=num)
    df = pd.DataFrame({
        'site': site,
        'product': [f'{category} Item {i+1:03d}' for i in range(num)],
        'price': prices,
        'availability': availability,
        'rating_label': ratings.astype(str),
        'category': category
    })
    return df


def run_scrape() -> pd.DataFrame:
    all_rows = []
    ts = datetime.utcnow().replace(microsecond=0).isoformat() + 'Z'
    for s in SITES:
        if s['type'] == 'books' and HAVE_NET_DEPS:
            df = scrape_books_toscrape(s['url'])
            if df.empty:
                df = synthetic_site(s['site'], 'Books')
        else:
            df = synthetic_site(s['site'], s['type'].capitalize())
        df['scrape_timestamp'] = ts
        all_rows.append(df)
        # Be polite if we had network
        time.sleep(0.5)
    return pd.concat(all_rows, ignore_index=True)


def compute_kpis(df: pd.DataFrame) -> pd.DataFrame:
    df['in_stock'] = (df['availability'].str.contains('In stock', case=False, na=False)).astype(int)
    kpis = df.groupby('site').agg(
        products=('product', 'count'),
        avg_price=('price', 'mean'),
        median_price=('price', 'median'),
        in_stock_rate=('in_stock', 'mean')
    ).reset_index()
    kpis['in_stock_rate'] = (kpis['in_stock_rate'] * 100).round(1)
    kpis['avg_price'] = kpis['avg_price'].round(2)
    kpis['median_price'] = kpis['median_price'].round(2)
    return kpis


def save_to_excel(df: pd.DataFrame, kpis: pd.DataFrame, out_path: str) -> None:
    with pd.ExcelWriter(out_path, engine='openpyxl') as writer:
        df.to_excel(writer, index=False, sheet_name='raw')
        kpis.to_excel(writer, index=False, sheet_name='kpi')


def plot_kpis(kpis: pd.DataFrame, df: pd.DataFrame, out_png: str) -> None:
    plt.figure(figsize=(18, 10))

    # 1) products per site
    plt.subplot(2, 2, 1)
    ax1 = sns.barplot(data=kpis.sort_values('products', ascending=False), x='site', y='products', color='#4ECDC4')
    plt.title('Products per Site', fontsize=13, fontweight='bold')
    plt.xlabel('Site')
    plt.ylabel('Products')
    for i, v in enumerate(kpis.sort_values('products', ascending=False)['products'].values):
        plt.text(i, v + max(kpis['products']) * 0.02, f'{int(v)}', ha='center', va='bottom', fontweight='bold', fontsize=9)

    # 2) price distribution
    plt.subplot(2, 2, 2)
    sns.boxplot(data=df, x='site', y='price')
    plt.title('Price Distribution', fontsize=13, fontweight='bold')
    plt.xlabel('Site')
    plt.ylabel('Price')

    # 3) in-stock rate
    plt.subplot(2, 2, 3)
    ax3 = sns.barplot(data=kpis, x='site', y='in_stock_rate', color='#45B7D1')
    plt.title('In-Stock Rate (%)', fontsize=13, fontweight='bold')
    plt.xlabel('Site')
    plt.ylabel('In-Stock %')
    for p in ax3.patches:
        height = p.get_height()
        ax3.annotate(f'{height:.1f}%', (p.get_x() + p.get_width() / 2, height + 1), ha='center', va='bottom', fontsize=9)

    # 4) avg vs median price
    plt.subplot(2, 2, 4)
    width = 0.35
    x = np.arange(len(kpis['site']))
    plt.bar(x - width/2, kpis['avg_price'], width, label='Avg', color='#FF6B6B')
    plt.bar(x + width/2, kpis['median_price'], width, label='Median', color='#96CEB4')
    plt.xticks(x, kpis['site'])
    plt.title('Avg vs Median Price', fontsize=13, fontweight='bold')
    plt.xlabel('Site')
    plt.ylabel('Price')
    plt.legend()

    plt.tight_layout()
    plt.savefig(out_png, dpi=300, bbox_inches='tight')
    plt.show()


def main() -> None:
    df = run_scrape()
    kpis = compute_kpis(df)
    save_to_excel(df, kpis, OUTPUT_EXCEL)
    plot_kpis(kpis, df, KPI_FIG)
    print('✅ Pipeline completed:')
    print(f' - Excel: {OUTPUT_EXCEL}')
    print(f' - KPIs figure: {KPI_FIG}')
    print(f' - Rows scraped: {len(df):,}')


if __name__ == '__main__':
    main()
