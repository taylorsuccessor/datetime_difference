from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_validation_empty_json():
    response = client.post("/api/difference-between-dates/", json={})
    assert response.status_code == 422

