import pandas as pd

def extract_features(df: pd.DataFrame) -> pd.DataFrame:
    """
    Extracts features from the raw input dataframe to prevent training-serving skew.
    Expected columns in df: 'store_id', 'item_id', 'date', 'promotion'
    """
    df = df.copy()
    
    # Ensure date is datetime
    if not pd.api.types.is_datetime64_any_dtype(df['date']):
        df['date'] = pd.to_datetime(df['date'])
        
    df['day_of_week'] = df['date'].dt.dayofweek
    df['month'] = df['date'].dt.month
    
    # Select final features for the model
    features = ['store_id', 'item_id', 'day_of_week', 'month', 'promotion']
    return df[features]
