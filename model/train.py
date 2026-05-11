import lightgbm as lgb
import pandas as pd
import numpy as np
import os
import datetime
import json
from sklearn.metrics import mean_squared_error, mean_absolute_error
from sklearn.model_selection import train_test_split
from api.features import extract_features

def fetch_data_from_bq():
    from google.cloud import bigquery
    project_id = os.getenv("GCP_PROJECT_ID")
    if not project_id:
        print("GCP_PROJECT_ID not set. Falling back to dummy data generation.")
        return generate_dummy_data()
        
    try:
        client = bigquery.Client(project=project_id)
        query = f"SELECT * FROM `{project_id}.demand_forecasting_data.training_data`"
        df = client.query(query).to_dataframe()
        print(f"Successfully loaded {len(df)} rows from BigQuery.")
        return df
    except Exception as e:
        print(f"Failed to load from BigQuery: {e}. Falling back to dummy data.")
        return generate_dummy_data()

def generate_dummy_data(n_samples=1000):
    np.random.seed(42)
    end_date = datetime.date.today()
    start_date = end_date - datetime.timedelta(days=365)
    dates = pd.date_range(start=start_date, end=end_date, periods=n_samples)
    
    data = {
        'store_id': np.random.randint(1, 10, n_samples),
        'item_id': np.random.randint(1, 50, n_samples),
        'date': dates,
        'promotion': np.random.choice([0, 1], n_samples),
    }
    df = pd.DataFrame(data)
    
    day_of_week = df['date'].dt.dayofweek
    month = df['date'].dt.month
    
    demand = (
        20 + df['store_id'] * 5 + df['item_id'] * 0.5 + df['promotion'] * 15
        + day_of_week * 2 + month * 1.5 + np.random.normal(0, 5, n_samples)
    )
    df['demand'] = np.maximum(0, demand)
    return df

def train_model():
    print("Fetching training data...")
    raw_df = fetch_data_from_bq()
    
    print("Extracting features...")
    X = extract_features(raw_df)
    y = raw_df['demand']
    
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    
    print("Training LightGBM model...")
    train_data = lgb.Dataset(X_train, label=y_train)
    test_data = lgb.Dataset(X_test, label=y_test, reference=train_data)
    
    params = {
        'objective': 'regression',
        'metric': 'rmse',
        'num_leaves': 31,
        'learning_rate': 0.05,
        'feature_fraction': 0.9,
        'verbose': -1
    }
    
    model = lgb.train(
        params, 
        train_data, 
        num_boost_round=100,
        valid_sets=[test_data],
        callbacks=[lgb.early_stopping(stopping_rounds=10)]
    )
    
    print("Evaluating model...")
    preds = model.predict(X_test)
    rmse = mean_squared_error(y_test, preds, squared=False)
    mae = mean_absolute_error(y_test, preds)
    print(f"Validation RMSE: {rmse:.4f}")
    print(f"Validation MAE: {mae:.4f}")
    
    os.makedirs('model/model_artifacts', exist_ok=True)
    
    # Versioning
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    versioned_path = f'model/model_artifacts/lgb_model_{timestamp}.txt'
    latest_path = 'model/model_artifacts/lgb_model.txt'
    
    model.save_model(versioned_path)
    model.save_model(latest_path) # Overwrite latest for serving
    
    # Save metrics
    metrics = {
        "timestamp": timestamp,
        "rmse": rmse,
        "mae": mae,
        "model_version": versioned_path
    }
    with open(f'model/model_artifacts/metrics_{timestamp}.json', 'w') as f:
        json.dump(metrics, f, indent=4)
        
    print(f"Model successfully saved to {latest_path} and {versioned_path}")

if __name__ == "__main__":
    train_model()
