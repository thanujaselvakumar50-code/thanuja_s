import os

os.environ["MOCK_MODE"] = "true"
os.environ["GEMINI_API_KEY"] = ""

from fastapi.testclient import TestClient
from backend.main import app

client = TestClient(app)


def test_root():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json()["status"] == "running"


def test_health():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "healthy"
    assert response.json()["mock_mode"] is True


def test_generate():
    payload = {
        "document_type": "Freelance Work Contract",
        "parties": "Jane Doe (Service Provider), TechNova Inc. (Client)",
        "terms": "Payment within 30 days; Confidentiality must be maintained; Either party may terminate with 15 days notice",
        "dates": "April 10, 2025",
        "language": "English",
    }
    response = client.post("/generate", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert data["success"] is True
    assert "Freelance Work Contract" in data["document"]
