import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots

# Set font for better readability
plt.rcParams['font.family'] = 'DejaVu Sans'

# Generate sample data
np.random.seed(42)

# Sales data
dates = pd.date_range('2024-01-01', periods=30, freq='D')
regions = ['Istanbul', 'Ankara', 'Izmir', 'Bursa', 'Antalya']
categories = ['Electronics', 'Fashion', 'Home & Living', 'Sports', 'Books']

sales_data = []
for date in dates:
    for region in regions:
        for category in categories:
            sales_data.append({
                'Date': date,
                'Region': region,
                'Category': category,
                'SalesAmount': np.random.randint(5000, 50000),
                'TargetAmount': np.random.randint(6000, 60000),
                'SalesQuantity': np.random.randint(50, 300)
            })

df_sales = pd.DataFrame(sales_data)

# Customer data
customer_data = []
segments = ['Premium', 'Gold', 'Silver', 'Bronze']
age_groups = ['18-24', '25-34', '35-44', '45-54', '55+']
genders = ['Male', 'Female']

for i in range(100):
    customer_data.append({
        'CustomerID': f'C{i+1:03d}',
        'Segment': np.random.choice(segments, p=[0.2, 0.3, 0.3, 0.2]),
        'AgeGroup': np.random.choice(age_groups, p=[0.2, 0.3, 0.25, 0.2, 0.05]),
        'Gender': np.random.choice(genders, p=[0.5, 0.5]),
        'TotalSpend': np.random.randint(2000, 25000),
        'SatisfactionScore': np.random.randint(1, 11),
        'ChurnStatus': np.random.choice(['Active', 'Churned'], p=[0.8, 0.2])
    })

df_customers = pd.DataFrame(customer_data)

# 1. Sales Trends (Line Chart)
plt.figure(figsize=(15, 10))

plt.subplot(2, 2, 1)
daily_sales = df_sales.groupby('Date')['SalesAmount'].sum()
plt.plot(daily_sales.index, daily_sales.values, linewidth=2, marker='o')
plt.title('Daily Sales Trends', fontsize=14, fontweight='bold')
plt.xlabel('Date')
plt.ylabel('Sales Amount (TL)')
plt.xticks(rotation=45)
plt.grid(True, alpha=0.3)

# 2. Regional Performance (Bar Chart)
plt.subplot(2, 2, 2)
regional_sales = df_sales.groupby('Region')['SalesAmount'].sum().sort_values(ascending=False)
bars = plt.bar(regional_sales.index, regional_sales.values, color=['#FF6B6B', '#4ECDC4', '#45B7D1', '#96CEB4', '#FFEAA7'])
plt.title('Regional Sales Performance', fontsize=14, fontweight='bold')
plt.xlabel('Region')
plt.ylabel('Total Sales (TL)')
plt.xticks(rotation=45)

# Add values on bars
for bar in bars:
    height = bar.get_height()
    plt.text(bar.get_x() + bar.get_width()/2., height + 1000,
             f'{height:,.0f}', ha='center', va='bottom')

# 3. Product Category Analysis (Horizontal Bar)
plt.subplot(2, 2, 3)
category_sales = df_sales.groupby('Category')['SalesAmount'].sum().sort_values()
bars = plt.barh(category_sales.index, category_sales.values, color=['#FF9999', '#66B2FF', '#99FF99', '#FFCC99', '#FF99CC'])
plt.title('Product Category Sales Analysis', fontsize=14, fontweight='bold')
plt.xlabel('Total Sales (TL)')

# Add values on bars
for i, bar in enumerate(bars):
    width = bar.get_width()
    plt.text(width + 1000, bar.get_y() + bar.get_height()/2,
             f'{width:,.0f}', ha='left', va='center')

# 4. Target vs Actual (Scatter Plot)
plt.subplot(2, 2, 4)
plt.scatter(df_sales['TargetAmount'], df_sales['SalesAmount'], 
           alpha=0.6, c=df_sales['SalesAmount'], cmap='viridis')
plt.plot([df_sales['TargetAmount'].min(), df_sales['TargetAmount'].max()], 
         [df_sales['TargetAmount'].min(), df_sales['TargetAmount'].max()], 
         'r--', linewidth=2, label='Target = Actual')
plt.title('Target vs Actual Sales', fontsize=14, fontweight='bold')
plt.xlabel('Target Amount (TL)')
plt.ylabel('Actual Amount (TL)')
plt.legend()
plt.colorbar(label='Sales Amount')

plt.tight_layout()
plt.savefig('sales_analysis.png', dpi=300, bbox_inches='tight')
plt.show()

# 5. Customer Segmentation (Pie Chart)
plt.figure(figsize=(15, 10))

plt.subplot(2, 2, 1)
segment_counts = df_customers['Segment'].value_counts()
colors = ['#FF6B6B', '#4ECDC4', '#45B7D1', '#96CEB4']
wedges, texts, autotexts = plt.pie(segment_counts.values, labels=segment_counts.index, 
                                   autopct='%1.1f%%', colors=colors, startangle=90)
plt.title('Customer Segmentation', fontsize=14, fontweight='bold')

# 6. Age Group and Gender Distribution (Stacked Bar)
plt.subplot(2, 2, 2)
age_gender_pivot = pd.crosstab(df_customers['AgeGroup'], df_customers['Gender'])
age_gender_pivot.plot(kind='bar', stacked=True, ax=plt.gca(), 
                      color=['#FF6B6B', '#4ECDC4'])
plt.title('Age Group and Gender Distribution', fontsize=14, fontweight='bold')
plt.xlabel('Age Group')
plt.ylabel('Customer Count')
plt.xticks(rotation=45)
plt.legend(title='Gender')

# 7. Customer Satisfaction Scores (Histogram)
plt.subplot(2, 2, 3)
plt.hist(df_customers['SatisfactionScore'], bins=10, color='#45B7D1', alpha=0.7, edgecolor='black')
plt.title('Customer Satisfaction Scores Distribution', fontsize=14, fontweight='bold')
plt.xlabel('Satisfaction Score')
plt.ylabel('Customer Count')
plt.grid(True, alpha=0.3)

# 8. Segment-based Average Spending (Box Plot)
plt.subplot(2, 2, 4)
df_customers.boxplot(column='TotalSpend', by='Segment', ax=plt.gca())
plt.title('Segment-based Spending Distribution', fontsize=14, fontweight='bold')
plt.xlabel('Segment')
plt.ylabel('Total Spending (TL)')
plt.suptitle('')  # Remove automatic title in boxplot

plt.tight_layout()
plt.savefig('customer_analysis.png', dpi=300, bbox_inches='tight')
plt.show()

# 9. Interactive Plotly Dashboard
fig = make_subplots(
    rows=2, cols=2,
    subplot_titles=('Sales Trends', 'Regional Performance', 'Category Analysis', 'Target vs Actual'),
    specs=[[{"type": "scatter"}, {"type": "bar"}],
           [{"type": "bar"}, {"type": "scatter"}]]
)

# Sales trends
fig.add_trace(
    go.Scatter(x=daily_sales.index, y=daily_sales.values, mode='lines+markers', name='Daily Sales'),
    row=1, col=1
)

# Regional performance
fig.add_trace(
    go.Bar(x=regional_sales.index, y=regional_sales.values, name='Regional Sales'),
    row=1, col=2
)

# Category analysis
fig.add_trace(
    go.Bar(x=category_sales.index, y=category_sales.values, name='Category Sales'),
    row=2, col=1
)

# Target vs actual
fig.add_trace(
    go.Scatter(x=df_sales['TargetAmount'], y=df_sales['SalesAmount'], 
               mode='markers', name='Target vs Actual'),
    row=2, col=2
)

fig.update_layout(height=800, title_text="Power BI Dashboard Examples")
fig.show()

print("✅ Visualizations created successfully!")
print("📊 Sales analysis charts: sales_analysis.png")
print("👥 Customer analysis charts: customer_analysis.png")
print("🎯 Interactive dashboard: Created with Plotly")
