import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from pathlib import Path
from sklearn.ensemble import RandomForestRegressor
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_absolute_error, r2_score

plt.style.use('seaborn-v0_8')
sns.set_palette('Set2')

OUTPUT_DIR = Path('.')
RANDOM_SEED = 42
np.random.seed(RANDOM_SEED)


def synthesize_data(days: int = 900) -> pd.DataFrame:
    dates = pd.date_range('2019-01-01', periods=days, freq='D')
    t = np.arange(days)

    # Climate generators (seasonal patterns + noise)
    temp = 18 + 10*np.sin(2*np.pi*t/365) + np.random.normal(0, 1.2, days)
    humidity = 60 + 20*np.sin(2*np.pi*(t-45)/365) + np.random.normal(0, 3.0, days)
    rainfall = np.clip(np.random.gamma(shape=2.0, scale=2.5, size=days) * (0.6 + 0.4*np.sin(2*np.pi*(t-90)/365)), 0, None)

    # Biological response: oviposition index (eggs) influenced by climate with lags
    # Eggs increase with temp (up to a point), high humidity, and rainfall from prior weeks
    base = 20 + 0.8*np.maximum(temp-20, 0) + 0.3*(humidity-50)
    lag7 = np.roll(rainfall, 7) * 0.9
    lag14 = np.roll(rainfall, 14) * 0.6
    eggs = base + lag7 + lag14 + np.random.normal(0, 3.0, days)
    eggs = np.clip(eggs, 0, None)

    df = pd.DataFrame({
        'date': dates,
        'temperature': temp,
        'humidity': humidity,
        'rainfall': rainfall,
        'eggs': eggs
    })
    return df


def engineer_features(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()
    df = df.sort_values('date')
    # Lags
    for l in [7, 14, 21]:
        df[f'rainfall_lag_{l}'] = df['rainfall'].shift(l)
        df[f'temp_lag_{l}'] = df['temperature'].shift(l)
        df[f'hum_lag_{l}'] = df['humidity'].shift(l)
    # Rolling means
    for w in [7, 14]:
        df[f'rainfall_roll_{w}'] = df['rainfall'].rolling(w).mean()
        df[f'temp_roll_{w}'] = df['temperature'].rolling(w).mean()
        df[f'hum_roll_{w}'] = df['humidity'].rolling(w).mean()
    # Seasonality (month, weekofyear)
    df['month'] = df['date'].dt.month
    df['doy_sin'] = np.sin(2*np.pi*df['date'].dt.dayofyear/365)
    df['doy_cos'] = np.cos(2*np.pi*df['date'].dt.dayofyear/365)

    df = df.dropna().reset_index(drop=True)
    return df


def train_evaluate(df_feat: pd.DataFrame):
    # Time-based split (last 20% as test)
    n = len(df_feat)
    split = int(n * 0.8)
    train, test = df_feat.iloc[:split], df_feat.iloc[split:]

    target = 'eggs'
    feature_cols = [c for c in df_feat.columns if c not in ['date', target]]

    X_train, y_train = train[feature_cols], train[target]
    X_test, y_test = test[feature_cols], test[target]

    # Baseline linear regression
    lin = LinearRegression()
    lin.fit(X_train, y_train)
    pred_lin = lin.predict(X_test)

    # RandomForest
    rf = RandomForestRegressor(n_estimators=300, max_depth=12, random_state=RANDOM_SEED, n_jobs=-1)
    rf.fit(X_train, y_train)
    pred_rf = rf.predict(X_test)

    metrics = pd.DataFrame([
        {'model': 'LinearRegression', 'MAE': mean_absolute_error(y_test, pred_lin), 'R2': r2_score(y_test, pred_lin)},
        {'model': 'RandomForest', 'MAE': mean_absolute_error(y_test, pred_rf), 'R2': r2_score(y_test, pred_rf)},
    ])

    return (lin, rf), (pred_lin, pred_rf), metrics, (train, test, feature_cols)


def plot_seasonality(df: pd.DataFrame, out_path: Path):
    plt.figure(figsize=(10, 6))
    monthly = df.set_index('date')['eggs'].resample('M').mean()
    plt.plot(monthly.index, monthly.values, color='#FF6B6B', linewidth=2.5)
    plt.title('Monthly Average Eggs (Seasonality)', fontsize=14, fontweight='bold')
    plt.xlabel('Month')
    plt.ylabel('Egg Index')
    plt.grid(True, alpha=0.3)
    plt.tight_layout()
    plt.savefig(out_path, dpi=300, bbox_inches='tight')
    plt.show()


def plot_pred_vs_actual(test: pd.DataFrame, preds: np.ndarray, out_path: Path, title: str):
    plt.figure(figsize=(12, 6))
    plt.plot(test['date'], test['eggs'], label='Actual', color='#4ECDC4', linewidth=2.5)
    plt.plot(test['date'], preds, label='Predicted', color='#FF6B6B', linewidth=2.0)
    plt.title(title, fontsize=14, fontweight='bold')
    plt.xlabel('Date')
    plt.ylabel('Egg Index')
    plt.legend()
    plt.grid(True, alpha=0.3)
    plt.tight_layout()
    plt.savefig(out_path, dpi=300, bbox_inches='tight')
    plt.show()


def plot_feature_importance(model: RandomForestRegressor, feature_names: list, out_path: Path):
    imp = pd.Series(model.feature_importances_, index=feature_names).sort_values(ascending=False)[:20]
    plt.figure(figsize=(10, 8))
    sns.barplot(x=imp.values, y=imp.index, color='#96CEB4')
    plt.title('Top Feature Importances (RandomForest)', fontsize=14, fontweight='bold')
    plt.xlabel('Importance')
    plt.ylabel('Feature')
    plt.tight_layout()
    plt.savefig(out_path, dpi=300, bbox_inches='tight')
    plt.show()


def main():
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    df = synthesize_data()
    df.to_csv(OUTPUT_DIR / 'mosquito_timeseries.csv', index=False)

    df_feat = engineer_features(df)
    (lin, rf), (pred_lin, pred_rf), metrics, (train, test, feature_cols) = train_evaluate(df_feat)

    # Save metrics
    metrics.to_csv(OUTPUT_DIR / 'model_metrics.csv', index=False)

    # Plots
    plot_seasonality(df, OUTPUT_DIR / 'seasonality_plot.png')
    plot_pred_vs_actual(test[['date', 'eggs']], pred_lin, OUTPUT_DIR / 'pred_vs_actual_linear.png', 'Pred vs Actual - Linear Regression')
    plot_pred_vs_actual(test[['date', 'eggs']], pred_rf, OUTPUT_DIR / 'pred_vs_actual_rf.png', 'Pred vs Actual - Random Forest')
    plot_feature_importance(rf, feature_cols, OUTPUT_DIR / 'feature_importance.png')

    print('✅ Modeling complete:')
    print(' - mosquito_timeseries.csv')
    print(' - model_metrics.csv')
    print(' - seasonality_plot.png')
    print(' - pred_vs_actual_linear.png')
    print(' - pred_vs_actual_rf.png')
    print(' - feature_importance.png')


if __name__ == '__main__':
    main()
