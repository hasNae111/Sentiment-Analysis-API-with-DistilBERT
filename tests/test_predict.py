from fastapi.testclient import TestClient
import app.main as main
import app.model as model

client = TestClient(main.app)

def test_predict_success(monkeypatch):
    # Evite de télécharger le modèle dans le test : on se moque de la fonction analyze
    def fake_analyze(text):
        return [{"label":"POSITIVE","score":0.95}]
    monkeypatch.setattr(model, "analyze", fake_analyze)
    resp = client.post("/predict", json={"text":"I love it"})
    assert resp.status_code == 200
    data = resp.json()
    assert data["sentiment"] == "POSITIVE"
    assert 0 <= data["confidence"] <= 1
