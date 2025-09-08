from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_predict_empty_text():
    resp = client.post("/predict", json={"text": ""})
    assert resp.status_code == 400
    assert "Text cannot be empty" in resp.json()["detail"]
