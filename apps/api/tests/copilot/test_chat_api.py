from fastapi.testclient import TestClient

from app.main import app


def test_copilot_chat_help_intent() -> None:
    client = TestClient(app)
    response = client.post("/api/v1/copilot/chat", json={"message": "help"})
    assert response.status_code == 200
    data = response.json()
    assert data["intent"] == "help"
    assert len(data["answer"]) > 10
    assert isinstance(data["follow_up_questions"], list)


def test_copilot_chat_general_fallback() -> None:
    client = TestClient(app)
    response = client.post("/api/v1/copilot/chat", json={"message": "xyzzy nothing"})
    assert response.status_code == 200
    data = response.json()
    assert data["intent"] == "general"


def test_copilot_chat_skills_intent_no_candidate() -> None:
    client = TestClient(app)
    response = client.post("/api/v1/copilot/chat", json={"message": "what skills do they have?"})
    assert response.status_code == 200
    data = response.json()
    assert data["intent"] == "skills"
    # Without a candidate the answer should indicate no candidate is loaded
    assert "candidate" in data["answer"].lower() or "provide" in data["answer"].lower()


def test_copilot_chat_risks_intent_no_candidate() -> None:
    client = TestClient(app)
    response = client.post("/api/v1/copilot/chat", json={"message": "what are the risks?"})
    assert response.status_code == 200
    data = response.json()
    assert data["intent"] == "risks"


def test_copilot_chat_recommendation_intent() -> None:
    client = TestClient(app)
    response = client.post("/api/v1/copilot/chat", json={"message": "should I hire this person?"})
    assert response.status_code == 200
    data = response.json()
    assert data["intent"] == "recommendation"
