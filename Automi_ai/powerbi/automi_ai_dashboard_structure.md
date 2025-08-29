# 🎯 Automi AI - Real Power BI Dashboard Structure

## 📊 MANUAL BUILD INSTRUCTIONS FOR POWER BI DESKTOP

### Step 1: Import Data
1. Open Power BI Desktop
2. Get Data → Text/CSV
3. Import these files:
   - `daily_defect_rate.csv`
   - `defects_by_cause.csv`
   - `defects_by_station_team.csv`
   - `throughput_by_station.csv`

### Step 2: Data Model Setup
1. **Create Date Table:**
   - New Table → `Date = CALENDAR(DATE(2022,1,1), DATE(2022,12,31))`
   - Mark as Date Table
   - Create relationships to all fact tables on `date` column

2. **Create Dimension Tables:**
   - Station = DISTINCT(defects_by_station_team[station])
   - Team = DISTINCT(defects_by_station_team[team])
   - Cause = DISTINCT(defects_by_cause[cause])

3. **Set Relationships:**
   - Date[Date] 1→* daily_defect_rate[date]
   - Date[Date] 1→* throughput_by_station[date]
   - Station[station] 1→* defects_by_station_team[station]
   - Team[team] 1→* defects_by_station_team[team]
   - Cause[cause] 1→* defects_by_cause[cause]

### Step 3: Create DAX Measures

#### Core Metrics:
```dax
Total Defects = SUM('defects_by_station_team'[defects])
Total Items = SUM('defects_by_station_team'[items])
Defect Rate = DIVIDE([Total Defects], [Total Items])
```

#### Time Intelligence:
```dax
Defects YoY = CALCULATE([Total Defects], DATEADD('Date'[Date], -1, YEAR))
Defect Rate YoY = CALCULATE([Defect Rate], DATEADD('Date'[Date], -1, YEAR))
Defects MoM = CALCULATE([Total Defects], DATEADD('Date'[Date], -1, MONTH))
```

#### Pareto Analysis:
```dax
Cause Defects = SUM('defects_by_cause'[defects])
Cause Rank = RANKX(ALL('defects_by_cause'[cause]), [Cause Defects], , DESC)
Cumulative % = 
VAR TotalAll = CALCULATE([Cause Defects], ALL('defects_by_cause'[cause]))
VAR Cum = CALCULATE([Cause Defects], 
    FILTER(ALL('defects_by_cause'[cause]), [Cause Rank] <= MAX([Cause Rank])))
RETURN DIVIDE(Cum, TotalAll)
```

### Step 4: Build Dashboard Pages

#### Page 1: Daily Quality Overview
- **Line Chart**: Date vs Defect Rate (from daily_defect_rate)
- **Line Chart**: Date vs Items (from daily_defect_rate)
- **Histogram**: Defect Rate Distribution
- **Bar Chart**: Monthly Average Defect Rate
- **Cards**: [Total Defects], [Total Items], [Defect Rate]

#### Page 2: Root Cause Analysis
- **Horizontal Bar**: Top 10 Defect Causes (defects_by_cause)
- **Bar Chart**: Defects by Cause (Pareto)
- **Line Chart**: Cumulative Defect % (using [Cumulative %] measure)
- **Slicer**: Date Range

#### Page 3: Station Performance
- **Matrix**: Station x Team with Defect Rate values
- **Bar Chart**: Top 5 Station Throughput (throughput_by_station)
- **Bar Chart**: Defect Rate by Station
- **Bar Chart**: Team Performance Comparison
- **Slicers**: Station, Team, Date

#### Page 4: Image Quality Metrics
- **Gauge**: Overall Defect Rate KPI
- **Pie Chart**: Defect Type Distribution (defects_by_cause)
- **Bar Chart**: Quality Score by Station (1 - Defect Rate)
- **Scatter Plot**: Production vs Quality (Items vs Defect Rate)
- **Cards**: Key Performance Indicators

### Step 5: Visual Configuration

#### Color Scheme:
- Primary: #FF6B6B (Red for defects)
- Secondary: #4ECDC4 (Teal for production)
- Accent: #45B7D1 (Blue for analysis)
- Success: #96CEB4 (Green for quality)

#### Conditional Formatting:
- Defect Rate: Red (High) → Yellow (Medium) → Green (Low)
- Quality Score: Green (High) → Yellow (Medium) → Red (Low)
- Heatmap: Red (High defect rate) → Green (Low defect rate)

#### Filters & Slicers:
- Date Range: Last 30 days, Last 90 days, Last 6 months
- Station: Multi-select with search
- Team: Multi-select with search
- Defect Cause: Top 10 with "Others" category

### Step 6: Save and Export
1. Save as `.pbix` file
2. Test all visuals and interactions
3. Verify data accuracy
4. Optimize performance
5. Ready for interview presentation

## 📋 Interview Talking Points

### Technical Skills Demonstrated:
- **Data Modeling**: Star schema with proper relationships
- **DAX**: Complex measures, time intelligence, Pareto analysis
- **Visualization**: Multiple chart types, conditional formatting
- **Performance**: Optimized data model and measures

### Business Insights:
- **Quality Trends**: Daily defect rate patterns
- **Root Cause Analysis**: Pareto principle application
- **Performance Metrics**: Station and team comparisons
- **Predictive Indicators**: Correlation analysis

### Project Impact:
- **Production Optimization**: Identify bottleneck stations
- **Quality Improvement**: Focus on top defect causes
- **Team Performance**: Benchmark and improvement areas
- **Cost Reduction**: Defect rate impact on production

---
*This is a REAL Power BI dashboard structure that you can manually build in Power BI Desktop using the provided CSV data files.*
