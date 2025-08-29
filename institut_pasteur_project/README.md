## Institut Pasteur – Climate Impact on Mosquito Oviposition (2021)

- Objective: Study climate impact (temperature, humidity, rainfall) on mosquito egg-laying cycles; build predictive models; provide interactive visualization.
- Data: Synthetic environmental and biological timeseries (daily) for 2+ years, with seasonal/lag effects.
- Methods: Pandas feature engineering (lags, rolling stats), scikit-learn (Linear/ElasticNet/RandomForest/XGB-like optional), time-based split, cross-validation.
- Viz: Matplotlib/Seaborn static charts; Streamlit app for interactive exploration.

Files
- `pasteur_modeling.py`: generates synthetic data, features, trains ML, saves metrics and charts.
- `app.py`: Streamlit app to interact with data and model predictions.
- Outputs: `mosquito_timeseries.csv`, `model_metrics.csv`, `feature_importance.png`, `seasonality_plot.png`, `pred_vs_actual.png`.

How to run
1) Create/activate env (already created earlier): `source ../data_analysis_env/bin/activate`
2) Install deps: `pip install scikit-learn streamlit`
3) Run modeling: `python pasteur_modeling.py`
4) Start app: `streamlit run app.py` (optional)

Interview talking points
- Seasonal/lagged climate effects are key drivers; rainfall spikes often precede egg peaks by ~7–14 days.
- Used time-based CV to avoid leakage; baseline vs ML uplift; feature importance highlights humidity × temperature interactions.
- Provided Streamlit for explainability and stakeholder access.
