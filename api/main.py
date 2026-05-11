from fastapi import FastAPI, Security, HTTPException
from fastapi.security.api_key import APIKeyHeader
from pydantic import BaseModel
# pyrefly: ignore [missing-import]
import lightgbm as lgb
import pandas as pd
import os
import datetime
import logging
import json

# Configure structured JSON logging
class JSONFormatter(logging.Formatter):
    def format(self, record):
        log_record = {
            "time": self.formatTime(record, self.datefmt),
            "level": record.levelname,
            "message": record.getMessage()
        }
        return json.dumps(log_record)

logger = logging.getLogger("api_logger")
logger.setLevel(logging.INFO)
handler = logging.StreamHandler()
handler.setFormatter(JSONFormatter())
logger.addHandler(handler)

# API Security configuration
API_KEY = os.getenv("API_KEY", "default-dev-key")
API_KEY_NAME = "X-API-Key"
api_key_header = APIKeyHeader(name=API_KEY_NAME, auto_error=False)

async def get_api_key(api_key_header: str = Security(api_key_header)):
    if api_key_header == API_KEY:
        return api_key_header
    else:
        logger.warning("Unauthorized access attempt")
        raise HTTPException(status_code=403, detail="Could not validate credentials")

app = FastAPI(
    title="Demand Forecasting API",
    description="API for serving LightGBM demand forecasting model",
    version="1.0.0"
)

# Load the model globally (defaulting to the local path if not in docker)
MODEL_PATH = os.getenv("MODEL_PATH", "../model/model_artifacts/lgb_model.txt")
model = None

@app.on_event("startup")
def load_model():
    global model
    try:
        model = lgb.Booster(model_file=MODEL_PATH)
        logger.info(f"Model loaded successfully from {MODEL_PATH}")
    except Exception as e:
        logger.error(f"Failed to load model: {e}. Are you sure you ran train.py first?")

class ForecastRequest(BaseModel):
    store_id: int
    item_id: int
    date: str
    promotion: int = 0

@app.get("/")
def read_root():
    return {"status": "ok", "message": "Demand Forecasting API is running."}

@app.post("/predict")
def predict_demand(request: ForecastRequest, api_key: str = Security(get_api_key)):
    if model is None:
        logger.error("Prediction attempted but model is not loaded.")
        raise HTTPException(status_code=503, detail="Model is not loaded.")
    
    try:
        # Parse date to extract features
        req_date = datetime.datetime.strptime(request.date, "%Y-%m-%d")
    except ValueError:
        logger.warning(f"Invalid date format received: {request.date}")
        raise HTTPException(status_code=400, detail="Invalid date format. Use YYYY-MM-DD.")
        
    try:
        # Prepare data for prediction matching our dummy training data
        input_df = pd.DataFrame([{
            'store_id': request.store_id,
            'item_id': request.item_id,
            'date': request.date,
            'promotion': request.promotion
        }])
        
        from features import extract_features
        input_data = extract_features(input_df)
        
        # Predict
        pred = model.predict(input_data)
        
        logger.info(f"Successful prediction for store={request.store_id}, item={request.item_id}")
        return {
            "store_id": request.store_id,
            "item_id": request.item_id,
            "date": request.date,
            "forecasted_demand": float(pred[0])
        }
    except Exception as e:
        logger.error(f"Prediction error: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal server error")
