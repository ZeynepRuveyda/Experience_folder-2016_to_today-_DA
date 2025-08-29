# 🎯 Guide Excel - Identification des Clients à Fort Potentiel (ISBANK)

## 📊 Structure des Données

### Colonnes de Base
- **CustomerID**: Identifiant unique du client
- **Age**: Âge du client
- **Income**: Revenu annuel
- **EducationLevel**: Niveau d'éducation
- **CurrentBalance**: Solde actuel du compte
- **MonthlyTransactions**: Nombre de transactions mensuelles
- **InvestmentAmount**: Montant des investissements

### Colonnes Calculées
- **IncomeScore**: Score basé sur le revenu (0-25)
- **BalanceScore**: Score basé sur le solde (0-25)
- **EducationScore**: Score basé sur l'éducation (0-25)
- **ActivityScore**: Score basé sur l'activité (0-25)
- **TotalScore**: Score total (0-100)
- **Segment**: Segment de client basé sur le score
- **PotentialLevel**: Niveau de potentiel (A+, A, B+, B, C)
- **CLV**: Customer Lifetime Value calculé

## 🔢 Formules Excel

### 1. Score Revenu (IncomeScore)
```excel
=IF(Income>100000,25,
  IF(Income>75000,20,
    IF(Income>50000,15,
      IF(Income>30000,10,5))))
```

**Logique:**
- Revenu > 100,000 TL → 25 points
- Revenu > 75,000 TL → 20 points
- Revenu > 50,000 TL → 15 points
- Revenu > 30,000 TL → 10 points
- Revenu ≤ 30,000 TL → 5 points

### 2. Score Solde (BalanceScore)
```excel
=IF(CurrentBalance>200000,25,
  IF(CurrentBalance>100000,20,
    IF(CurrentBalance>50000,15,
      IF(CurrentBalance>25000,10,5))))
```

**Logique:**
- Solde > 200,000 TL → 25 points
- Solde > 100,000 TL → 20 points
- Solde > 50,000 TL → 15 points
- Solde > 25,000 TL → 10 points
- Solde ≤ 25,000 TL → 5 points

### 3. Score Éducation (EducationScore)
```excel
=IF(EducationLevel="PhD",25,
  IF(EducationLevel="Master",20,
    IF(EducationLevel="Bachelor",15,10)))
```

**Logique:**
- PhD → 25 points
- Master → 20 points
- Bachelor → 15 points
- High School → 10 points

### 4. Score Activité (ActivityScore)
```excel
=IF(MonthlyTransactions>40,25,
  IF(MonthlyTransactions>30,20,
    IF(MonthlyTransactions>20,15,
      IF(MonthlyTransactions>10,10,5))))
```

**Logique:**
- Transactions > 40 → 25 points
- Transactions > 30 → 20 points
- Transactions > 20 → 15 points
- Transactions > 10 → 10 points
- Transactions ≤ 10 → 5 points

### 5. Score Total (TotalScore)
```excel
=IncomeScore+BalanceScore+EducationScore+ActivityScore
```

**Résultat:** Score de 0 à 100 points

### 6. Segment Client (Segment)
```excel
=IF(TotalScore>=80,"Ultra High Potential",
  IF(TotalScore>=70,"High Potential",
    IF(TotalScore>=60,"Medium-High Potential",
      IF(TotalScore>=50,"Medium Potential","Standard Potential"))))
```

**Logique:**
- Score 80-100 → Ultra High Potential
- Score 70-79 → High Potential
- Score 60-69 → Medium-High Potential
- Score 50-59 → Medium Potential
- Score 0-49 → Standard Potential

### 7. Niveau de Potentiel (PotentialLevel)
```excel
=IF(TotalScore>=80,"A+",
  IF(TotalScore>=70,"A",
    IF(TotalScore>=60,"B+",
      IF(TotalScore>=50,"B","C"))))
```

**Logique:**
- Score 80-100 → A+
- Score 70-79 → A
- Score 60-69 → B+
- Score 50-59 → B
- Score 0-49 → C

### 8. Customer Lifetime Value (CLV)
```excel
=((Income*0.1)+(CurrentBalance*0.05)+(InvestmentAmount*0.15))*(1+(TotalScore/100)*0.5)
```

**Formule détaillée:**
- **Base CLV** = (Revenu × 0.1) + (Solde × 0.05) + (Investissement × 0.15)
- **Multiplicateur** = 1 + (Score_Total / 100) × 0.5
- **CLV Final** = Base CLV × Multiplicateur

## 📈 Exemples de Calculs

### Client C0001 (Score: 80)
- **Revenu:** 85,000 TL → Score: 20
- **Solde:** 150,000 TL → Score: 20
- **Éducation:** Master → Score: 20
- **Activité:** 35 transactions → Score: 20
- **Total:** 20+20+20+20 = **80 points**
- **Segment:** Ultra High Potential
- **Niveau:** A+
- **CLV:** ((85000×0.1)+(150000×0.05)+(25000×0.15))×(1+(80/100)×0.5) = **12,500 TL**

### Client C0006 (Score: 55)
- **Revenu:** 45,000 TL → Score: 15
- **Solde:** 60,000 TL → Score: 15
- **Éducation:** High School → Score: 10
- **Activité:** 20 transactions → Score: 15
- **Total:** 15+15+10+15 = **55 points**
- **Segment:** Medium Potential
- **Niveau:** B
- **CLV:** ((45000×0.1)+(60000×0.05)+(10000×0.15))×(1+(55/100)×0.5) = **6,750 TL**

## 🎨 Formatage Conditionnel

### Score Total
- **Vert (80-100):** Ultra High Potential
- **Bleu (70-79):** High Potential
- **Jaune (60-69):** Medium-High Potential
- **Orange (50-59):** Medium Potential
- **Rouge (0-49):** Standard Potential

### CLV
- **Vert:** CLV > 15,000 TL
- **Bleu:** CLV 10,000-15,000 TL
- **Jaune:** CLV 7,500-10,000 TL
- **Orange:** CLV 5,000-7,500 TL
- **Rouge:** CLV < 5,000 TL

## 📊 Tableaux de Bord

### 1. Résumé par Segment
```excel
=COUNTIFS(Segment,"Ultra High Potential")
=COUNTIFS(Segment,"High Potential")
=AVERAGEIFS(CLV,Segment,"Ultra High Potential")
```

### 2. Distribution des Scores
```excel
=COUNTIFS(TotalScore,">=80")
=COUNTIFS(TotalScore,">=70")
=COUNTIFS(TotalScore,">=60")
```

### 3. CLV Moyen par Segment
```excel
=AVERAGEIFS(CLV,Segment,"Ultra High Potential")
=AVERAGEIFS(CLV,Segment,"High Potential")
=AVERAGEIFS(CLV,Segment,"Medium-High Potential")
```

## 🔍 Filtres Recommandés

### Filtre 1: Clients à Fort Potentiel
- **TotalScore** ≥ 70
- **Segment** = "High Potential" OU "Ultra High Potential"

### Filtre 2: Opportunités d'Upgrade
- **TotalScore** 60-69
- **EducationLevel** = "Bachelor" OU "High School"
- **Age** < 45

### Filtre 3: Clients Premium
- **TotalScore** ≥ 80
- **CLV** > 15,000 TL
- **CurrentBalance** > 150,000 TL

## 💡 Conseils d'Utilisation

1. **Mise à jour mensuelle** des données
2. **Validation** des scores avec l'équipe commerciale
3. **Ajustement** des seuils selon les objectifs
4. **Suivi** des conversions par segment
5. **Optimisation** des offres par niveau de potentiel

## 🚀 Avantages de cette Approche

- ✅ **Transparente:** Logique claire et compréhensible
- ✅ **Modifiable:** Facile d'ajuster les critères
- ✅ **Automatisée:** Calculs automatiques en Excel
- ✅ **Traçable:** Historique complet des scores
- ✅ **Actionable:** Recommandations claires par segment
