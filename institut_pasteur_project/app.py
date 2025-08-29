import streamlit as st
import pandas as pd
import numpy as np
import altair as alt
from pathlib import Path

st.set_page_config(page_title='Institut Pasteur – Mosquito Oviposition', layout='wide')

st.title('Institut Pasteur – Climate Impact on Mosquito Oviposition')
st.caption('Synthetic demo for interview – explore climate variables and egg-laying index')

DATA_CSV = Path('mosquito_timeseries.csv')
METRICS_CSV = Path('model_metrics.csv')

@st.cache_data
def load_data():
    if DATA_CSV.exists():
        df = pd.read_csv(DATA_CSV, parse_dates=['date'])
    else:
        df = pd.DataFrame()
    metrics = pd.read_csv(METRICS_CSV) if METRICS_CSV.exists() else pd.DataFrame()
    return df, metrics


df, metrics = load_data()
if df.empty:
    st.warning('Run pasteur_modeling.py first to generate data and metrics.')
    st.stop()

with st.sidebar:
    st.header('Filters')
    date_min = st.date_input('Start date', df['date'].min().date())
    date_max = st.date_input('End date', df['date'].max().date())
    subset = df[(df['date'] >= pd.to_datetime(date_min)) & (df['date'] <= pd.to_datetime(date_max))]

st.subheader('Time Series')
line = alt.Chart(subset).mark_line().encode(
    x='date:T', y='eggs:Q', tooltip=['date:T', 'eggs:Q', 'temperature:Q', 'humidity:Q', 'rainfall:Q']
).properties(height=250)

cols = st.columns(1)
cols[0].altair_chart(line, use_container_width=True)

st.subheader('Climate vs Eggs')
left, right = st.columns(2)

scatter1 = alt.Chart(subset).mark_circle(opacity=0.5).encode(
    x='temperature:Q', y='eggs:Q', color=alt.value('#FF6B6B'), tooltip=['temperature', 'eggs']
).properties(height=250)
left.altair_chart(scatter1, use_container_width=True)

scatter2 = alt.Chart(subset).mark_circle(opacity=0.5).encode(
    x='rainfall:Q', y='eggs:Q', color=alt.value('#4ECDC4'), tooltip=['rainfall', 'eggs']
).properties(height=250)
right.altair_chart(scatter2, use_container_width=True)

st.subheader('Model Metrics')
if not metrics.empty:
    st.dataframe(metrics.style.format({'MAE': '{:.2f}', 'R2': '{:.3f}'}), use_container_width=True)
else:
    st.info('Metrics not found yet.')
