# 🚀 Automi AI - Power BI Dashboard Setup Guide

## 📊 Dashboard Overview
This guide will help you create a professional Power BI dashboard for the Automi AI production quality analysis project.

## 📁 Data Sources
Import these CSV files from `powerbi_exports/` folder:
1. **`daily_defect_rate.csv`** - Daily production and defect metrics
2. **`defects_by_cause.csv`** - Root cause analysis data
3. **`defects_by_station_team.csv`** - Station and team performance
4. **`throughput_by_station.csv`** - Production throughput by station

## 🎯 Dashboard Structure

### Page 1: Daily Quality Overview
- **Line Chart**: Daily Defect Rate Trend (Date vs Defect Rate)
- **Line Chart**: Daily Production Volume (Date vs Items)
- **Histogram**: Defect Rate Distribution
- **Bar Chart**: Monthly Average Defect Rate
- **Cards**: Total Defects, Total Items, Overall Defect Rate

### Page 2: Root Cause Analysis
- **Horizontal Bar**: Top 10 Defect Causes
- **Bar Chart**: Defects by Cause (Pareto)
- **Bar Chart**: Defect Rate by Cause (%)
- **Line Chart**: Cumulative Defect Percentage
- **Slicer**: Date Range

### Page 3: Station Performance
- **Heatmap**: Station x Team Defect Rate Matrix
- **Bar Chart**: Top 5 Station Throughput
- **Bar Chart**: Defect Rate by Station
- **Bar Chart**: Team Performance Comparison
- **Slicers**: Station, Team, Date

### Page 4: Image Quality Metrics
- **Gauge**: Overall Defect Rate KPI
- **Pie Chart**: Defect Type Distribution
- **Bar Chart**: Quality Score by Station
- **Scatter Plot**: Production vs Quality Correlation
- **Cards**: Key Performance Indicators

## 🔧 Data Model Setup

### 1. Create Date Dimension
```sql
-- Create Date table
Date = CALENDAR(DATE(2022,1,1), DATE(2022,12,31))
```
- Mark as Date table
- Create relationships to all fact tables on `date` column

### 2. Create Dimension Tables
```sql
-- Station Dimension
Station = DISTINCT(defects_by_station_team[station])

-- Team Dimension  
Team = DISTINCT(defects_by_station_team[team])

-- Cause Dimension
Cause = DISTINCT(defects_by_cause[cause])
```

### 3. Set Up Relationships
- Date[Date] 1→* daily_defect_rate[date]
- Date[Date] 1→* throughput_by_station[date]
- Station[station] 1→* defects_by_station_team[station]
- Team[team] 1→* defects_by_station_team[team]
- Cause[cause] 1→* defects_by_cause[cause]

## 📈 DAX Measures

### Core Metrics
```dax
Total Defects = SUM('defects_by_station_team'[defects])
Total Items = SUM('defects_by_station_team'[items])
Defect Rate = DIVIDE([Total Defects], [Total Items])
```

### Time Intelligence
```dax
Defects YoY = CALCULATE([Total Defects], DATEADD('Date'[Date], -1, YEAR))
Defect Rate YoY = CALCULATE([Defect Rate], DATEADD('Date'[Date], -1, YEAR))
Defects MoM = CALCULATE([Total Defects], DATEADD('Date'[Date], -1, MONTH))
```

### Pareto Analysis
```dax
Cause Defects = SUM('defects_by_cause'[defects])
Cause Rank = RANKX(ALL('defects_by_cause'[cause]), [Cause Defects], , DESC)
Cumulative % = 
VAR TotalAll = CALCULATE([Cause Defects], ALL('defects_by_cause'[cause]))
VAR Cum = CALCULATE([Cause Defects], 
    FILTER(ALL('defects_by_cause'[cause]), [Cause Rank] <= MAX([Cause Rank])))
RETURN DIVIDE(Cum, TotalAll)
```

### Performance Metrics
```dax
Station Defect Rate = AVERAGE('defects_by_station_team'[defect_rate])
Team Defect Rate = AVERAGE('defects_by_station_team'[defect_rate])
Quality Score = (1 - [Defect Rate]) * 100
```

## 🎨 Visual Configuration

### Color Scheme
- **Primary**: #FF6B6B (Red for defects)
- **Secondary**: #4ECDC4 (Teal for production)
- **Accent**: #45B7D1 (Blue for analysis)
- **Success**: #96CEB4 (Green for quality)

### Conditional Formatting
- **Defect Rate**: Red (High) → Yellow (Medium) → Green (Low)
- **Quality Score**: Green (High) → Yellow (Medium) → Red (Low)
- **Heatmap**: Red (High defect rate) → Green (Low defect rate)

### Filters & Slicers
- **Date Range**: Last 30 days, Last 90 days, Last 6 months
- **Station**: Multi-select with search
- **Team**: Multi-select with search
- **Defect Cause**: Top 10 with "Others" category

## 📱 Mobile & Responsive Design
- Use responsive layouts
- Optimize for mobile viewing
- Ensure touch-friendly interactions
- Test on different screen sizes

## 🔄 Refresh & Maintenance
- **Data Refresh**: Daily (if source data updates)
- **Performance**: Use aggregations for large datasets
- **Backup**: Save multiple versions of .pbix file
- **Documentation**: Keep measure definitions updated

## 🚀 Publishing Steps
1. **Test**: Verify all visuals work correctly
2. **Optimize**: Check performance and loading times
3. **Publish**: Upload to Power BI Service
4. **Share**: Create app for team access
5. **Schedule**: Set up automatic refresh

## 📋 Pre-Interview Checklist
- [ ] All 4 CSV files imported
- [ ] Date dimension created and marked
- [ ] Relationships properly configured
- [ ] DAX measures working correctly
- [ ] Visuals displaying accurate data
- ** [ ] Dashboard ready for presentation
- [ ] Key insights documented
- [ ] Performance optimized

## 💡 Key Insights to Highlight
1. **Overall defect rate trend** (improving/declining)
2. **Top 3 defect causes** and their impact
3. **Best/worst performing stations** and teams
4. **Seasonal patterns** in defect rates
5. **Correlation** between production volume and quality
6. **Cost implications** of defects (if data available)

## 🔗 Related Files
- **HTML Dashboards**: Interactive Plotly versions
- **PNG Visuals**: Static charts for documentation
- **CSV Data**: Raw data for analysis
- **Python Scripts**: Data generation and processing

---
*This dashboard demonstrates your expertise in Power BI, data modeling, DAX, and production quality analysis.*
