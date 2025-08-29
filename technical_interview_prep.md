# Technical Interview Preparation Guide

## 🔍 **Power BI Technical Questions**

### **1. DAX Formulas**
**Question:** "How would you calculate year-over-year sales growth?"
**Answer:**
```dax
Sales Growth = 
VAR CurrentYearSales = CALCULATE(SUM(Sales[Amount]), YEAR(Sales[Date]) = YEAR(TODAY()))
VAR PreviousYearSales = CALCULATE(SUM(Sales[Amount]), YEAR(Sales[Date]) = YEAR(TODAY()) - 1)
RETURN
DIVIDE(CurrentYearSales - PreviousYearSales, PreviousYearSales)
```

### **2. Data Modeling**
**Question:** "What's the difference between star schema and snowflake schema?"
**Answer:**
- **Star Schema**: Central fact table with dimension tables around it
- **Snowflake Schema**: Dimension tables are normalized
- **Advantage**: Star schema has faster query performance
- **Disadvantage**: Snowflake uses less storage

### **3. Performance Optimization**
**Question:** "How do you optimize performance in Power BI?"
**Answer:**
- Use incremental refresh
- Remove unnecessary columns
- Use measures instead of calculated columns
- Optimize query folding
- Use aggregations

---

## 🐍 **Python Technical Questions**

### **1. Data Manipulation**
**Question:** "How do you handle missing values in Pandas?"
**Answer:**
```python
import pandas as pd
import numpy as np

# Check missing values
df.isnull().sum()

# Drop missing values
df.dropna()

# Fill missing values
df.fillna(method='ffill')  # Forward fill
df.fillna(df.mean())       # Fill with mean
df.fillna(df.median())     # Fill with median
```

### **2. Data Visualization**
**Question:** "What's the difference between Matplotlib and Seaborn?"
**Answer:**
- **Matplotlib**: Low-level, highly customizable
- **Seaborn**: High-level, built on matplotlib, statistical plots
- **Seaborn**: Better default styling
- **Matplotlib**: More control options

### **3. Machine Learning**
**Question:** "How do you prevent overfitting?"
**Answer:**
```python
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score

# Use cross-validation
from sklearn.model_selection import cross_val_score

# Add regularization
# Do hyperparameter tuning
# Use early stopping
```

---

## 🗄️ **SQL Technical Questions**

### **1. Complex Queries**
**Question:** "When would you use window functions?"
**Answer:**
```sql
-- Calculate running total
SELECT 
    date,
    sales,
    SUM(sales) OVER (ORDER BY date) as running_total
FROM sales_table;

-- Calculate rank
SELECT 
    product,
    sales,
    RANK() OVER (ORDER BY sales DESC) as rank
FROM products;
```

### **2. Performance Tuning**
**Question:** "How do you optimize SQL query performance?"
**Answer:**
- Proper indexing
- Avoid SELECT *
- Use EXISTS instead of IN
- Limit result sets
- Use appropriate JOIN types
- Analyze execution plans

### **3. Data Warehouse Concepts**
**Question:** "What's the difference between fact table and dimension table?"
**Answer:**
- **Fact Table**: Measures, metrics, numerical data
- **Dimension Table**: Descriptive attributes, categorical data
- **Fact Table**: Many rows
- **Dimension Table**: Fewer rows, more columns

---

## 📊 **Data Analysis Process**

### **1. Data Collection**
**Question:** "How do you collect data from different sources?"
**Answer:**
- **Databases**: SQL queries, connection strings
- **APIs**: REST APIs, authentication, rate limiting
- **Files**: CSV, Excel, JSON, XML
- **Web Scraping**: BeautifulSoup, Selenium
- **Streaming**: Kafka, real-time data

### **2. Data Cleaning**
**Question:** "How do you solve data quality problems?"
**Answer:**
- **Missing Values**: Imputation, deletion
- **Outliers**: IQR method, z-score
- **Duplicates**: Remove, merge
- **Data Types**: Convert, validate
- **Consistency**: Business rules, validation

### **3. Data Analysis**
**Question:** "What do you do in Exploratory Data Analysis?"
**Answer:**
- **Descriptive Statistics**: Mean, median, std
- **Data Distribution**: Histograms, box plots
- **Correlation Analysis**: Correlation matrix
- **Missing Data Analysis**: Patterns, reasons
- **Outlier Detection**: Statistical methods

---

## 🚀 **Advanced Topics**

### **1. ETL Processes**
**Question:** "What stages are in an ETL pipeline?"
**Answer:**
- **Extract**: Data sources, APIs, databases
- **Transform**: Cleaning, aggregation, enrichment
- **Load**: Target systems, data warehouses
- **Monitoring**: Logging, error handling
- **Scheduling**: Cron jobs, automation

### **2. Data Governance**
**Question:** "How do you ensure data security and privacy?"
**Answer:**
- **Access Control**: Role-based permissions
- **Data Encryption**: At rest, in transit
- **Audit Logging**: Track data access
- **Compliance**: GDPR, HIPAA, SOX
- **Data Masking**: PII protection

### **3. Cloud Technologies**
**Question:** "How do you do data analysis in the cloud?"
**Answer:**
- **AWS**: Redshift, S3, Glue, QuickSight
- **Azure**: Synapse, Data Factory, Power BI
- **GCP**: BigQuery, Dataflow, Looker
- **Benefits**: Scalability, cost-effectiveness
- **Challenges**: Security, compliance

---

## 📝 **Interview Tips**

### **1. Use STAR Method**
- **Situation**: Explain the problem
- **Task**: Define the task
- **Action**: Describe what you did
- **Result**: State the result and impact

### **2. Show Technical Details**
- Give code examples
- Draw architecture diagrams
- Mention performance metrics
- Emphasize business impact

### **3. Ask Questions**
- Learn about project details
- Ask about team structure
- Learn about technology stack
- Research growth opportunities

### **4. Prepare Portfolio**
- GitHub repositories
- Power BI dashboards
- Project documentation
- Code samples
- Performance metrics
