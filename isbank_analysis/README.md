# 🏦 ISBANK - Identification des Clients à Fort Potentiel

## 📁 Contenu du Dossier

Ce dossier contient l'analyse complète pour identifier les clients à fort potentiel chez ISBANK, utilisant une approche Excel + Python.

## 📊 Fichiers d'Analyse

### 1. **`isbank_simple_analysis.py`**
- Code Python principal utilisant uniquement matplotlib
- Logique de scoring simplifiée (style Excel)
- Génération de 2 visualisations principales

### 2. **`isbank_scoring_logic_excel.csv`**
- Exemple de données avec 20 clients
- Tous les scores calculés automatiquement
- Format prêt pour Excel

### 3. **`excel_scoring_guide.md`**
- Guide complet des formules Excel
- Logique de scoring détaillée
- Exemples de calculs

## 🎨 Visualisations Créées

### **`isbank_simple_analysis.png`**
- Dashboard principal de scoring
- Distribution des scores totaux
- Segmentation des clients
- Composantes du score
- CLV vs Score total

### **`isbank_detailed_analysis.png`**
- Analyse détaillée par segment
- Comparaison CLV par niveau
- Corrélation entre composantes
- Distribution par niveau de potentiel

## 🎯 Logique de Scoring

### **Système de Points (0-100)**
- **Score Revenu (0-25):** 5 catégories de revenu
- **Score Solde (0-25):** 5 catégories de solde
- **Score Éducation (0-25):** PhD=25, Master=20, Bachelor=15, HS=10
- **Score Activité (0-25):** 5 catégories de transactions

### **Segmentation Automatique**
- **A+ (80-100):** Ultra High Potential
- **A (70-79):** High Potential
- **B+ (60-69):** Medium-High Potential
- **B (50-59):** Medium Potential
- **C (0-49):** Standard Potential

### **Formule CLV**
```
CLV = (Revenu × 0.1) + (Solde × 0.05) + (Investissement × 0.15) × Multiplicateur
Multiplicateur = 1 + (Score_Total / 100) × 0.5
```

## 🚀 Utilisation

### **Pour l'Entretien:**
1. Expliquer la logique de scoring (4 critères)
2. Montrer la segmentation automatique
3. Démontrer le calcul CLV
4. Présenter les visualisations

### **Pour Excel:**
1. Ouvrir `isbank_scoring_logic_excel.csv`
2. Suivre le guide `excel_scoring_guide.md`
3. Appliquer les formules de scoring
4. Créer des tableaux de bord

### **Pour Python:**
1. Exécuter `isbank_simple_analysis.py`
2. Modifier les seuils de scoring
3. Ajuster les poids des critères
4. Générer de nouvelles visualisations

## 💡 Points Clés pour l'Entretien

- ✅ **Logique transparente** (comme Excel)
- ✅ **4 critères objectifs** de scoring
- ✅ **Seuil 70+** pour haut potentiel
- ✅ **Segmentation automatique** A+, A, B+, B, C
- ✅ **CLV avec multiplicateur** basé sur le score
- ✅ **Visualisations claires** avec matplotlib

## 📈 Résultats Attendus

- **Clients à Fort Potentiel:** Score ≥ 70
- **Multiplicateur CLV:** 1.5x à 2.5x
- **Segmentation:** 15-20% High Potential
- **ROI:** Amélioration des offres ciblées

---
*Créé pour l'entretien ISBANK - Data Analyst Position*
*Focus: Identification des clients à fort potentiel*
