import pytest
import json
from app import app, get_relevant_chunks

@pytest.fixture
def client():
    app.config["TESTING"] = True
    with app.test_client() as client:
        yield client

#  Test FAISS retrieval
def test_faiss_retrieval():
    query = "What are cyclical stocks?"
    results = get_relevant_chunks(query, k=3)
    
    assert isinstance(results, list)
    assert len(results) > 0  # Ensure results are returned
    assert isinstance(results[0], str)  # Ensure results are strings

#  Test /chat endpoint
def test_chat_endpoint(client):
    response = client.post("/chat", data=json.dumps({"query": "Tell me about cyclical stocks."}),
                           content_type="application/json")

    assert response.status_code == 200
    data = response.get_json()
    assert "answer" in data
    assert "retrieved_chunks" in data

#  Test /chat with empty input
def test_chat_empty_query(client):
    response = client.post("/chat", data=json.dumps({"query": ""}),
                           content_type="application/json")
    assert response.status_code == 400

#  Test /history endpoint
def test_history_endpoint(client):
    response = client.get("/history")
    
    assert response.status_code == 200
    data = response.get_json()
    assert isinstance(data, list)  # Should return a list of chat history
