from fastapi.testclient import TestClient
from api.main import app, API_KEY

client = TestClient(app)

def test_read_root():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"status": "ok", "message": "Demand Forecasting API is running."}

def test_predict_no_auth():
    response = client.post("/predict", json={"store_id": 1, "item_id": 1, "date": "2023-01-01", "promotion": 0})
    assert response.status_code == 403

def test_predict_auth_no_model():
    response = client.post(
        "/predict", 
        json={"store_id": 1, "item_id": 1, "date": "2023-01-01", "promotion": 0},
        headers={"X-API-Key": API_KEY}
    )
    assert response.status_code in [200, 503]

def test_predict_invalid_date():
    response = client.post(
        "/predict", 
        json={"store_id": 1, "item_id": 1, "date": "invalid-date", "promotion": 0},
        headers={"X-API-Key": API_KEY}
    )
    assert response.status_code == 400