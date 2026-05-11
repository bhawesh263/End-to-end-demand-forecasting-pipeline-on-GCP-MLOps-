import pandas as pd
import numpy as np
from google.cloud import bigquery
import os
import datetime

def generate_dummy_data(n_samples=1000):
    np.random.seed(42)
    # Generate dates over the past year
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
    
    # Calculate demand based on derived features to simulate real patterns
    day_of_week = df['date'].dt.dayofweek
    month = df['date'].dt.month
    
    demand = (
        20 
        + df['store_id'] * 5 
        + df['item_id'] * 0.5
        + df['promotion'] * 15
        + day_of_week * 2  # higher demand on weekends
        + month * 1.5      # slight seasonality
        + np.random.normal(0, 5, n_samples)
    )
    
    df['demand'] = np.maximum(0, demand)
    return df

def upload_to_bigquery():
    project_id = os.getenv("GCP_PROJECT_ID", "your-project-id")
    dataset_id = "demand_forecasting_data"
    table_id = "training_data"
    
    client = bigquery.Client(project=project_id)
    table_ref = f"{project_id}.{dataset_id}.{table_id}"
    
    print(f"Generating data...")
    df = generate_dummy_data(5000)
    
    print(f"Uploading to {table_ref}...")
    job_config = bigquery.LoadJobConfig(
        write_disposition="WRITE_TRUNCATE", # Overwrite if exists
    )
    
    try:
        job = client.load_table_from_dataframe(
            df, table_ref, job_config=job_config
        )
        job.result()  # Wait for the job to complete.
        print(f"Uploaded {len(df)} rows to {table_ref}.")
    except Exception as e:
        print(f"Error uploading to BigQuery: {e}")
        print("Note: Ensure you have authenticated with GCP using 'gcloud auth application-default login'")

if __name__ == "__main__":
    upload_to_bigquery()
