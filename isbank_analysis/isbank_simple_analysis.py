import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# Set style for professional look
plt.style.use('default')
plt.rcParams['font.size'] = 10
plt.rcParams['figure.figsize'] = (12, 8)

# Generate simplified high-potential customer data for ISBANK
np.random.seed(42)

# Customer data with high-potential indicators
customer_data = []
for i in range(1000):
    # Customer demographics
    age = np.random.randint(25, 70)
    income = np.random.lognormal(10.5, 0.6)
    education_level = np.random.choice(['High School', 'Bachelor', 'Master', 'PhD'], 
                                     p=[0.3, 0.4, 0.2, 0.1])
    
    # Financial behavior indicators
    current_balance = np.random.lognormal(8, 1.2)
    monthly_transactions = np.random.poisson(25)
    investment_amount = np.random.lognormal(7, 1.5)
    
    # High-potential scoring logic (Excel-like approach)
    # Score 1: Income Score (0-25 points)
    if income > 100000:
        income_score = 25
    elif income > 75000:
        income_score = 20
    elif income > 50000:
        income_score = 15
    elif income > 30000:
        income_score = 10
    else:
        income_score = 5
    
    # Score 2: Balance Score (0-25 points)
    if current_balance > 200000:
        balance_score = 25
    elif current_balance > 100000:
        balance_score = 20
    elif current_balance > 50000:
        balance_score = 15
    elif current_balance > 25000:
        balance_score = 10
    else:
        balance_score = 5
    
    # Score 3: Education Score (0-25 points)
    if education_level == 'PhD':
        education_score = 25
    elif education_level == 'Master':
        education_score = 20
    elif education_level == 'Bachelor':
        education_score = 15
    else:
        education_score = 10
    
    # Score 4: Activity Score (0-25 points)
    if monthly_transactions > 40:
        activity_score = 25
    elif monthly_transactions > 30:
        activity_score = 20
    elif monthly_transactions > 20:
        activity_score = 15
    elif monthly_transactions > 10:
        activity_score = 10
    else:
        activity_score = 5
    
    # Total Potential Score (0-100)
    total_score = income_score + balance_score + education_score + activity_score
    
    # Customer segment based on total score
    if total_score >= 80:
        segment = 'Ultra High Potential'
        potential_level = 'A+'
    elif total_score >= 70:
        segment = 'High Potential'
        potential_level = 'A'
    elif total_score >= 60:
        segment = 'Medium-High Potential'
        potential_level = 'B+'
    elif total_score >= 50:
        segment = 'Medium Potential'
        potential_level = 'B'
    else:
        segment = 'Standard Potential'
        potential_level = 'C'
    
    # CLV calculation (Excel-like formula)
    # CLV = (Income × 0.1) + (Balance × 0.05) + (Investment × 0.15) × Score_Multiplier
    base_clv = (income * 0.1) + (current_balance * 0.05) + (investment_amount * 0.15)
    score_multiplier = 1 + (total_score / 100) * 0.5
    customer_lifetime_value = base_clv * score_multiplier
    
    customer_data.append({
        'CustomerID': f'C{i+1:04d}',
        'Age': age,
        'Income': income,
        'EducationLevel': education_level,
        'CurrentBalance': current_balance,
        'MonthlyTransactions': monthly_transactions,
        'InvestmentAmount': investment_amount,
        'IncomeScore': income_score,
        'BalanceScore': balance_score,
        'EducationScore': education_score,
        'ActivityScore': activity_score,
        'TotalScore': total_score,
        'Segment': segment,
        'PotentialLevel': potential_level,
        'CustomerLifetimeValue': customer_lifetime_value
    })

df_customers = pd.DataFrame(customer_data)

# Create comprehensive visualizations using only matplotlib

# 1. High-Potential Customer Scoring Dashboard
fig, axes = plt.subplots(2, 3, figsize=(18, 12))
fig.suptitle('ISBANK - Identification des Clients à Fort Potentiel\n(Logique Excel + Python)', 
             fontsize=16, fontweight='bold')

# 1.1 Total Score Distribution
axes[0, 0].hist(df_customers['TotalScore'], bins=20, color='#FF6B6B', alpha=0.7, edgecolor='black')
axes[0, 0].axvline(x=70, color='red', linestyle='--', linewidth=2, label='Seuil Haut Potentiel (70+)')
axes[0, 0].set_title('Distribution des Scores Totaux', fontweight='bold')
axes[0, 0].set_xlabel('Score Total (0-100)')
axes[0, 0].set_ylabel('Nombre de Clients')
axes[0, 0].legend()
axes[0, 0].grid(True, alpha=0.3)

# 1.2 Customer Segments
segment_counts = df_customers['Segment'].value_counts()
colors = ['#2CA02C', '#FFD700', '#FF7F0E', '#D62728', '#9467BD']
wedges, texts, autotexts = axes[0, 1].pie(segment_counts.values, labels=segment_counts.index, 
                                           autopct='%1.1f%%', colors=colors, startangle=90)
axes[0, 1].set_title('Segmentation des Clients', fontweight='bold')
for autotext in autotexts:
    autotext.set_color('white')
    autotext.set_fontweight('bold')

# 1.3 Score Components Breakdown
score_components = ['IncomeScore', 'BalanceScore', 'EducationScore', 'ActivityScore']
avg_scores = [df_customers[col].mean() for col in score_components]
component_names = ['Revenu', 'Solde', 'Éducation', 'Activité']

bars = axes[0, 2].bar(component_names, avg_scores, color=['#FF6B6B', '#4ECDC4', '#45B7D1', '#96CEB4'])
axes[0, 2].set_title('Scores Moyens par Composante', fontweight='bold')
axes[0, 2].set_ylabel('Score Moyen (0-25)')
axes[0, 2].set_ylim(0, 25)

# Add values on bars
for bar in bars:
    height = bar.get_height()
    axes[0, 2].text(bar.get_x() + bar.get_width()/2., height + 0.5,
                     f'{height:.1f}', ha='center', va='bottom', fontweight='bold')

# 1.4 CLV vs Total Score
scatter = axes[1, 0].scatter(df_customers['TotalScore'], df_customers['CustomerLifetimeValue'], 
                             c=df_customers['TotalScore'], cmap='viridis', alpha=0.6, s=30)
axes[1, 0].set_title('Score Total vs CLV', fontweight='bold')
axes[1, 0].set_xlabel('Score Total')
axes[1, 0].set_ylabel('Customer Lifetime Value (TL)')
axes[1, 0].grid(True, alpha=0.3)
plt.colorbar(scatter, ax=axes[1, 0], label='Score Total')

# 1.5 Age vs Potential Score
age_groups = pd.cut(df_customers['Age'], bins=[25, 35, 45, 55, 70], labels=['25-35', '36-45', '46-55', '56-70'])
age_potential = df_customers.groupby(age_groups)['TotalScore'].mean()
bars = axes[1, 1].bar(age_potential.index, age_potential.values, color='#4ECDC4')
axes[1, 1].set_title('Score de Potentiel par Groupe d\'Âge', fontweight='bold')
axes[1, 1].set_xlabel('Groupe d\'Âge')
axes[1, 1].set_ylabel('Score Moyen')
axes[1, 1].set_ylim(0, 100)

# Add values on bars
for bar in bars:
    height = bar.get_height()
    axes[1, 1].text(bar.get_x() + bar.get_width()/2., height + 1,
                     f'{height:.1f}', ha='center', va='bottom', fontweight='bold')

# 1.6 Education Impact on Potential
education_potential = df_customers.groupby('EducationLevel')['TotalScore'].mean().sort_values(ascending=False)
bars = axes[1, 2].bar(education_potential.index, education_potential.values, color='#45B7D1')
axes[1, 2].set_title('Impact de l\'Éducation sur le Potentiel', fontweight='bold')
axes[1, 2].set_xlabel('Niveau d\'Éducation')
axes[1, 2].set_ylabel('Score Moyen')
axes[1, 2].set_ylim(0, 100)
axes[1, 2].tick_params(axis='x', rotation=45)

# Add values on bars
for bar in bars:
    height = bar.get_height()
    axes[1, 2].text(bar.get_x() + bar.get_width()/2., height + 1,
                     f'{height:.1f}', ha='center', va='bottom', fontweight='bold')

plt.tight_layout()
plt.savefig('isbank_simple_analysis.png', dpi=300, bbox_inches='tight')
plt.show()

# 2. Detailed Score Analysis
fig, axes = plt.subplots(2, 2, figsize=(16, 12))
fig.suptitle('Analyse Détaillée des Scores - Logique Excel', fontsize=16, fontweight='bold')

# 2.1 Score Distribution by Segment
high_potential = df_customers[df_customers['TotalScore'] >= 70]
medium_potential = df_customers[(df_customers['TotalScore'] >= 50) & (df_customers['TotalScore'] < 70)]
low_potential = df_customers[df_customers['TotalScore'] < 50]

axes[0, 0].hist(high_potential['TotalScore'], bins=15, alpha=0.7, label='Haut Potentiel (70+)', color='#2CA02C')
axes[0, 0].hist(medium_potential['TotalScore'], bins=15, alpha=0.7, label='Potentiel Moyen (50-69)', color='#FFD700')
axes[0, 0].hist(low_potential['TotalScore'], bins=15, alpha=0.7, label='Potentiel Standard (<50)', color='#D62728')
axes[0, 0].set_title('Distribution des Scores par Segment', fontweight='bold')
axes[0, 0].set_xlabel('Score Total')
axes[0, 0].set_ylabel('Nombre de Clients')
axes[0, 0].legend()
axes[0, 0].grid(True, alpha=0.3)

# 2.2 CLV Comparison by Segment
segments = ['Haut Potentiel', 'Potentiel Moyen', 'Potentiel Standard']
clv_means = [
    high_potential['CustomerLifetimeValue'].mean(),
    medium_potential['CustomerLifetimeValue'].mean(),
    low_potential['CustomerLifetimeValue'].mean()
]
clv_stds = [
    high_potential['CustomerLifetimeValue'].std(),
    medium_potential['CustomerLifetimeValue'].std(),
    low_potential['CustomerLifetimeValue'].std()
]

bars = axes[0, 1].bar(segments, clv_means, yerr=clv_stds, capsize=5, 
                       color=['#2CA02C', '#FFD700', '#D62728'])
axes[0, 1].set_title('CLV Moyen par Segment', fontweight='bold')
axes[0, 1].set_ylabel('CLV Moyen (TL)')

# Add values on bars
for bar in bars:
    height = bar.get_height()
    axes[0, 1].text(bar.get_x() + bar.get_width()/2., height + height*0.01,
                     f'{height:,.0f}', ha='center', va='bottom', fontweight='bold')

# 2.3 Score Components Heatmap
score_matrix = df_customers[score_components].corr()
im = axes[1, 0].imshow(score_matrix, cmap='YlOrRd', aspect='auto')
axes[1, 0].set_title('Corrélation entre Composantes de Score', fontweight='bold')
axes[1, 0].set_xticks(range(len(component_names)))
axes[1, 0].set_yticks(range(len(component_names)))
axes[1, 0].set_xticklabels(component_names, rotation=45)
axes[1, 0].set_yticklabels(component_names)

# Add correlation values
for i in range(len(component_names)):
    for j in range(len(component_names)):
        text = axes[1, 0].text(j, i, f'{score_matrix.iloc[i, j]:.2f}',
                               ha="center", va="center", color="black", fontweight='bold')

plt.colorbar(im, ax=axes[1, 0], label='Corrélation')

# 2.4 Potential Level Distribution
potential_counts = df_customers['PotentialLevel'].value_counts().sort_index()
colors = ['#D62728', '#FF7F0E', '#FFD700', '#2CA02C', '#1F77B4']
bars = axes[1, 1].bar(potential_counts.index, potential_counts.values, color=colors)
axes[1, 1].set_title('Distribution par Niveau de Potentiel', fontweight='bold')
axes[1, 1].set_xlabel('Niveau de Potentiel')
axes[1, 1].set_ylabel('Nombre de Clients')

# Add values on bars
for bar in bars:
    height = bar.get_height()
    axes[1, 1].text(bar.get_x() + bar.get_width()/2., height + height*0.01,
                     f'{height:,.0f}', ha='center', va='bottom', fontweight='bold')

plt.tight_layout()
plt.savefig('isbank_detailed_analysis.png', dpi=300, bbox_inches='tight')
plt.show()

# 3. Summary and Excel Logic Explanation
print("\n" + "="*80)
print("🎯 LOGIQUE D'IDENTIFICATION DES CLIENTS À FORT POTENTIEL - ISBANK")
print("="*80)

print(f"\n📊 STATISTIQUES GÉNÉRALES:")
print(f"   • Total Clients: {len(df_customers):,}")
print(f"   • Clients à Fort Potentiel (Score ≥70): {len(high_potential):,}")
print(f"   • Pourcentage de Fort Potentiel: {len(high_potential)/len(df_customers)*100:.1f}%")

print(f"\n💰 VALEUR CLIENT:")
print(f"   • CLV Moyen (Tous): {df_customers['CustomerLifetimeValue'].mean():,.0f} TL")
print(f"   • CLV Moyen (Haut Potentiel): {high_potential['CustomerLifetimeValue'].mean():,.0f} TL")
print(f"   • Multiplicateur CLV: {high_potential['CustomerLifetimeValue'].mean()/df_customers['CustomerLifetimeValue'].mean():.2f}x")

print(f"\n🎯 LOGIQUE DE SCORING (Style Excel):")
print(f"   • Score Revenu (0-25): Basé sur 5 tranches de revenu")
print(f"   • Score Solde (0-25): Basé sur 5 tranches de solde")
print(f"   • Score Éducation (0-25): PhD=25, Master=20, Bachelor=15, HS=10")
print(f"   • Score Activité (0-25): Basé sur 5 tranches de transactions mensuelles")
print(f"   • Score Total = Somme des 4 composantes (0-100)")

print(f"\n📈 FORMULE CLV (Style Excel):")
print(f"   • CLV = (Revenu × 0.1) + (Solde × 0.05) + (Investissement × 0.15) × Multiplicateur")
print(f"   • Multiplicateur = 1 + (Score_Total / 100) × 0.5")

print(f"\n🔍 SEGMENTATION AUTOMATIQUE:")
print(f"   • A+ (80-100): Ultra High Potential")
print(f"   • A (70-79): High Potential")
print(f"   • B+ (60-69): Medium-High Potential")
print(f"   • B (50-59): Medium Potential")
print(f"   • C (0-49): Standard Potential")

print(f"\n💡 AVANTAGES DE CETTE APPROCHE:")
print(f"   • Logique simple et transparente (comme Excel)")
print(f"   • Facile à expliquer aux équipes commerciales")
print(f"   • Modifiable et adaptable")
print(f"   • Automatisation possible avec Python")
print(f"   • Traçabilité complète des scores")

print("\n✅ Visualisations créées avec succès!")
print("📊 Graphiques principaux: isbank_simple_analysis.png")
print("📈 Analyse détaillée: isbank_detailed_analysis.png")
print("💼 Parfait pour l'entretien - Logique Excel + Python expliquée!")
