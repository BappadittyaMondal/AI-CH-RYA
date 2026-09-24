"""
Integration and API Test Suite for AI ĀCHĀRYA
Tests FastAPI REST endpoints and end-to-end multi-agent orchestration.
"""

from fastapi.testclient import TestClient
from app.api.main import app

client = TestClient(app)


def test_api_health_endpoint():
    response = client.get("/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "healthy"
    assert "AI ĀCHĀRYA" in data["app"]


def test_api_daily_gurukula_endpoint():
    response = client.get("/daily-gurukula?day=1&mode=Student")
    assert response.status_code == 200
    data = response.json()
    assert data["day_number"] == 1
    assert "one_shloka" in data
    assert "one_sanskrit_word" in data
    assert "one_dharma_reflection" in data


def test_api_kala_endpoint():
    response = client.get("/kala/1")
    assert response.status_code == 200
    data = response.json()
    assert data["number"] == 1
    assert data["sanskrit_term"] == "गीतम्"


def test_api_quantum_verdict_endpoint():
    response = client.get("/quantum-verdict")
    assert response.status_code == 200
    data = response.json()
    assert data["standing_status"] == "NO_DEMONSTRATED_ADVANTAGE"


def test_api_verify_verse_endpoint():
    req_body = {
        "text_name": "Bhagavad Gītā",
        "chapter": "2",
        "verse": "47",
        "sanskrit_passage": "कर्मण्येवाधिकारस्ते मा फलेषु कदाचन।"
    }
    response = client.post("/verify-verse", json=req_body)
    assert response.status_code == 200
    data = response.json()
    assert data["passed"] is True
    assert "Verified" in data["safe_output_text"]


def test_api_query_endpoint():
    req_body = {
        "query": "What is the meaning of Gītā 2.47?",
        "mode": "Scholar"
    }
    response = client.post("/query", json=req_body)
    assert response.status_code == 200
    data = response.json()
    assert "structured_response" in data
    assert "rendered_markdown" in data
    assert "कर्मण्येवाधिकारस्ते" in data["rendered_markdown"]
