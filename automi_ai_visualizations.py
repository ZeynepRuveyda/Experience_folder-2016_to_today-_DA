import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots

# Set style for professional look
plt.style.use('seaborn-v0_8')
sns.set_palette("husl")

# Generate AI/ML focused data for Automi AI
np.random.seed(42)

# Customer behavior data for AI startup
dates = pd.date_range('2021-01-01', periods=365, freq='D')
customer_ids = [f'C{i:04d}' for i in range(1000)]

# Customer behavior patterns
customer_data = []
for customer_id in customer_ids:
    # Customer segments based on AI analysis
    segment = np.random.choice(['High Value', 'Medium Value', 'Low Value', 'Churn Risk'], 
                              p=[0.2, 0.4, 0.3, 0.1])
    
    # AI-predicted churn probability
    churn_prob = np.random.beta(2, 8) if segment == 'Churn Risk' else np.random.beta(8, 2)
    
    # Customer lifetime value prediction
    clv = np.random.lognormal(8, 1.5) if segment == 'High Value' else np.random.lognormal(6, 1.2)
    
    # Engagement metrics
    daily_usage = np.random.poisson(15) if segment == 'High Value' else np.random.poisson(5)
    
    customer_data.append({
        'CustomerID': customer_id,
        'Segment': segment,
        'ChurnProbability': churn_prob,
        'PredictedCLV': clv,
        'DailyUsage': daily_usage,
        'SatisfactionScore': np.random.randint(1, 11),
        'LastPurchaseDays': np.random.randint(1, 90),
        'TotalPurchases': np.random.poisson(20) if segment == 'High Value' else np.random.poisson(8)
    })

df_customers = pd.DataFrame(customer_data)

# AI model performance data
model_performance = []
for date in dates[::7]:  # Weekly data
    model_performance.append({
        'Date': date,
        'ChurnAccuracy': np.random.normal(0.85, 0.05),
        'CLVPredictionError': np.random.normal(0.12, 0.03),
        'ModelTrainingTime': np.random.normal(45, 10),
        'DataProcessingTime': np.random.normal(15, 3),
        'ActiveUsers': np.random.normal(850, 100)
    })

df_model = pd.DataFrame(model_performance)

# Create comprehensive visualizations for Automi AI

# 1. Customer Segmentation Analysis (AI-powered)
plt.figure(figsize=(20, 15))

# Customer segments distribution
plt.subplot(3, 3, 1)
segment_counts = df_customers['Segment'].value_counts()
colors = ['#FF6B6B', '#4ECDC4', '#45B7D1', '#96CEB4']
wedges, texts, autotexts = plt.pie(segment_counts.values, labels=segment_counts.index, 
                                   autopct='%1.1f%%', colors=colors, startangle=90)
plt.title('AI-Powered Customer Segmentation', fontsize=16, fontweight='bold')
plt.setp(autotexts, size=10, weight="bold")

# Churn probability distribution by segment
plt.subplot(3, 3, 2)
sns.boxplot(data=df_customers, x='Segment', y='ChurnProbability', palette=colors)
plt.title('Churn Risk Analysis by Segment', fontsize=14, fontweight='bold')
plt.xticks(rotation=45)
plt.ylabel('Churn Probability')

# Customer Lifetime Value prediction
plt.subplot(3, 3, 3)
sns.histplot(data=df_customers, x='PredictedCLV', hue='Segment', bins=30, palette=colors, alpha=0.7)
plt.title('Predicted Customer Lifetime Value', fontsize=14, fontweight='bold')
plt.xlabel('Predicted CLV ($)')
plt.ylabel('Customer Count')

# Daily usage patterns
plt.subplot(3, 3, 4)
usage_by_segment = df_customers.groupby('Segment')['DailyUsage'].mean().sort_values(ascending=False)
bars = plt.bar(usage_by_segment.index, usage_by_segment.values, color=colors)
plt.title('Average Daily Usage by Segment', fontsize=14, fontweight='bold')
plt.xticks(rotation=45)
plt.ylabel('Daily Usage (minutes)')

# Add values on bars
for bar in bars:
    height = bar.get_height()
    plt.text(bar.get_x() + bar.get_width()/2., height + 0.5,
             f'{height:.1f}', ha='center', va='bottom', fontweight='bold')

# Satisfaction vs Churn Risk
plt.subplot(3, 3, 5)
plt.scatter(df_customers['SatisfactionScore'], df_customers['ChurnProbability'], 
           c=df_customers['Segment'].map({'High Value': 0, 'Medium Value': 1, 'Low Value': 2, 'Churn Risk': 3}),
           cmap='viridis', alpha=0.6, s=50)
plt.colorbar(label='Segment')
plt.title('Satisfaction vs Churn Risk', fontsize=14, fontweight='bold')
plt.xlabel('Satisfaction Score')
plt.ylabel('Churn Probability')
plt.grid(True, alpha=0.3)

# Purchase frequency analysis
plt.subplot(3, 3, 6)
purchase_by_segment = df_customers.groupby('Segment')['TotalPurchases'].mean().sort_values(ascending=False)
bars = plt.bar(purchase_by_segment.index, purchase_by_segment.values, color=colors)
plt.title('Average Purchase Frequency by Segment', fontsize=14, fontweight='bold')
plt.xticks(rotation=45)
plt.ylabel('Total Purchases')

# Add values on bars
for bar in bars:
    height = bar.get_height()
    plt.text(bar.get_x() + bar.get_width()/2., height + 0.5,
             f'{height:.1f}', ha='center', va='bottom', fontweight='bold')

# AI Model Performance Over Time
plt.subplot(3, 3, 7)
plt.plot(df_model['Date'], df_model['ChurnAccuracy'], linewidth=3, marker='o', color='#FF6B6B', label='Churn Accuracy')
plt.plot(df_model['Date'], df_model['CLVPredictionError'], linewidth=3, marker='s', color='#4ECDC4', label='CLV Prediction Error')
plt.title('AI Model Performance Metrics', fontsize=14, fontweight='bold')
plt.xlabel('Date')
plt.ylabel('Performance Score')
plt.legend()
plt.grid(True, alpha=0.3)

# Model training efficiency
plt.subplot(3, 3, 8)
plt.plot(df_model['Date'], df_model['ModelTrainingTime'], linewidth=3, marker='^', color='#45B7D1', label='Training Time (min)')
plt.plot(df_model['Date'], df_model['DataProcessingTime'], linewidth=3, marker='d', color='#96CEB4', label='Processing Time (min)')
plt.title('Model Training & Processing Efficiency', fontsize=14, fontweight='bold')
plt.xlabel('Date')
plt.ylabel('Time (minutes)')
plt.legend()
plt.grid(True, alpha=0.3)

# User growth and engagement
plt.subplot(3, 3, 9)
plt.plot(df_model['Date'], df_model['ActiveUsers'], linewidth=3, marker='o', color='#FF9999', label='Active Users')
plt.title('Platform User Growth', fontsize=14, fontweight='bold')
plt.xlabel('Date')
plt.ylabel('Active Users')
plt.legend()
plt.grid(True, alpha=0.3)

plt.tight_layout()
plt.savefig('automi_ai_analysis.png', dpi=300, bbox_inches='tight')
plt.show()

# 2. Interactive Plotly Dashboard for Automi AI
fig = make_subplots(
    rows=3, cols=2,
    subplot_titles=('Customer Segmentation', 'Churn Risk Analysis', 'CLV Prediction', 
                    'Usage Patterns', 'Model Performance', 'User Growth'),
    specs=[[{"type": "pie"}, {"type": "scatter"}],
           [{"type": "bar"}, {"type": "histogram"}],
           [{"type": "scatter"}, {"type": "scatter"}]]
)

# Customer segmentation pie chart
fig.add_trace(
    go.Pie(labels=segment_counts.index, values=segment_counts.values, name="Segments"),
    row=1, col=1
)

# Churn probability scatter
fig.add_trace(
    go.Scatter(x=df_customers['SatisfactionScore'], y=df_customers['ChurnProbability'],
               mode='markers', name='Churn Risk',
               marker=dict(color=df_customers['Segment'].map({'High Value': 0, 'Medium Value': 1, 'Low Value': 2, 'Churn Risk': 3}),
                          colorscale='viridis', size=8)),
    row=1, col=2
)

# CLV by segment bar chart
fig.add_trace(
    go.Bar(x=df_customers.groupby('Segment')['PredictedCLV'].mean().index,
            y=df_customers.groupby('Segment')['PredictedCLV'].mean().values,
            name='Average CLV'),
    row=2, col=1
)

# Usage distribution histogram
fig.add_trace(
    go.Histogram(x=df_customers['DailyUsage'], nbinsx=30, name='Usage Distribution'),
    row=2, col=2
)

# Model performance over time
fig.add_trace(
    go.Scatter(x=df_model['Date'], y=df_model['ChurnAccuracy'],
               mode='lines+markers', name='Churn Accuracy'),
    row=3, col=1
)

# User growth
fig.add_trace(
    go.Scatter(x=df_model['Date'], y=df_model['ActiveUsers'],
               mode='lines+markers', name='Active Users'),
    row=3, col=2
)

fig.update_layout(height=1000, title_text="Automi AI - AI/ML Data Analysis Dashboard", 
                  showlegend=True)
fig.show()

print("✅ Automi AI visualizations created successfully!")
print("📊 AI/ML analysis charts: automi_ai_analysis.png")
print("🎯 Interactive dashboard: Created with Plotly")
print("💼 Perfect for AI/ML Data Analyst position interview!")

