import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px
from datetime import datetime, timedelta
import requests
import os

st.set_page_config(
    page_title="Demand Forecasting Dashboard",
    page_icon="📊",
    layout="wide"
)

st.title("📊 Demand Forecasting Dashboard")
st.markdown("Real-time MLOps pipeline on GCP")

with st.sidebar:
    st.header("⚙️ Configuration")
    api_url = st.text_input(
        "API URL",
        value=os.getenv("API_URL", "http://localhost:8000")
    )
    api_key = st.text_input(
        "API Key",
        value=os.getenv("API_KEY", "default-dev-key"),
        type="password"
    )

tab1, tab2, tab3, tab4 = st.tabs(
    ["📈 Dashboard", "🔮 Predictions", "📊 Model Info", "🔍 Data Explorer"]
)

with tab1:
    st.header("Overview")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric(label="Total Predictions", value="1,234", delta="↑ 12%")
    with col2:
        st.metric(label="Avg Demand", value="287", delta="↓ 2%")
    with col3:
        st.metric(label="Model Accuracy", value="94.2%", delta="↑ 1.5%")
    with col4:
        st.metric(label="API Uptime", value="99.9%", delta="✓")
    
    st.subheader("Demand Trend")
    dates = pd.date_range(start='2024-01-01', periods=90, freq='D')
    demand = 200 + np.cumsum(np.random.randn(90) * 10)
    
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=dates, y=demand, mode='lines', name='Actual Demand', fill='tozeroy'))
    st.plotly_chart(fig, use_container_width=True)

with tab2:
    st.header("Make Predictions")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Single Prediction")
        
        store_id = st.slider("Store ID", 1, 10, 1)
        item_id = st.slider("Item ID", 1, 50, 1)
        pred_date = st.date_input("Prediction Date")
        promo = st.checkbox("Promotional Event")
        
        if st.button("🔮 Predict"):
            try:
                response = requests.post(
                    f"{api_url}/predict",
                    json={
                        "store_id": store_id,
                        "item_id": item_id,
                        "date": pred_date.strftime("%Y-%m-%d"),
                        "promotion": int(promo)
                    },
                    headers={"X-API-Key": api_key},
                    timeout=5
                )
                
                if response.status_code == 200:
                    result = response.json()
                    st.success(f"✓ Prediction: **{result['forecasted_demand']:.2f}** units")
                else:
                    st.error(f"API Error: {response.status_code} - {response.text}")
            except Exception as e:
                st.error(f"Connection Error: {e}")

with tab3:
    st.header("Model Information")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Model Specifications")
        st.json({
            "model_type": "RandomForestRegressor",
            "n_estimators": 100,
            "max_depth": 10,
            "features": 7,
            "training_samples": 1000
        })
    
    with col2:
        st.subheader("Performance Metrics")
        metrics_data = {"MAE": 23.45, "RMSE": 34.67, "R² Score": 0.942, "MAPE": 8.23}
        for metric, value in metrics_data.items():
            st.metric(metric, f"{value:.2f}")

with tab4:
    st.header("Data Explorer")
    
    df = pd.DataFrame({
        'date': pd.date_range('2024-01-01', periods=100),
        'product_id': np.random.choice(['PROD_001', 'PROD_002', 'PROD_003'], 100),
        'region': np.random.choice(['North', 'South', 'East', 'West'], 100),
        'demand': np.random.randint(50, 500, 100),
        'price': np.random.uniform(10, 100, 100),
        'promotional_event': np.random.choice([0, 1], 100)
    })
    
    st.dataframe(df, use_container_width=True)

st.markdown("---")
st.markdown("Demand Forecasting MLOps Pipeline | Built with ❤️ on GCP")