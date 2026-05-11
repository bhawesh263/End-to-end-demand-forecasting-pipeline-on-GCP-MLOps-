import pandas as pd
from api.features import extract_features
from scripts.upload_dummy_data import generate_dummy_data

def test_feature_extraction():
    df = pd.DataFrame([{
        'store_id': 1,
        'item_id': 2,
        'date': '2023-01-01', # Sunday
        'promotion': 1
    }])
    features = extract_features(df)
    assert 'day_of_week' in features.columns
    assert 'month' in features.columns
    assert features['day_of_week'].iloc[0] == 6 # Sunday
    assert features['month'].iloc[0] == 1

def test_dummy_data_generation():
    df = generate_dummy_data(10)
    assert len(df) == 10
    assert 'demand' in df.columns
    assert (df['demand'] >= 0).all()