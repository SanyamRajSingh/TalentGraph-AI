import httpx
import time
import base64

API_URL = "http://127.0.0.1:8000/api/v1"

def run_e2e():
    client = httpx.Client(base_url=API_URL, timeout=30.0)
    
    print("1. Generate Role DNA...")
    role_res = client.post("/generate-role-dna", json={"job_description": "We need a Senior Backend Engineer who knows Python and PostgreSQL."})
    assert role_res.status_code == 200, role_res.text
    role_id = role_res.json()["role_id"]
    
    print("2. Upload Resume / Build Twin...")
    twin_res = client.post("/build-digital-twins", json={"resume_text": "Alice Engineer\nPython expert with 10 years experience in PostgreSQL."})
    assert twin_res.status_code == 200, twin_res.text
    candidate_id = twin_res.json()["candidate_id"]
    
    print("3. Evaluate...")
    eval_res = client.post("/evaluate", json={"role_id": role_id, "candidate_id": candidate_id})
    assert eval_res.status_code == 200, eval_res.text
    
    print("4. Rank...")
    # we don't have rank-candidates, we have /rank (wait, rank-candidates is 501, /rank is implemented)
    rank_res = client.post("/rank", json={"role_id": role_id, "candidate_ids": [candidate_id]})
    assert rank_res.status_code == 200, rank_res.text
    
    print("5. Generate Explanations...")
    exp_res = client.post("/generate-explanations", json={"role_id": role_id, "rankings": [{"candidate_id": candidate_id, "rank": 1, "score": 95}]})
    assert exp_res.status_code == 200, exp_res.text
    
    print("6. Generate Recommendations...")
    rec_res = client.post("/recommend", json={"role_id": role_id, "candidate_id": candidate_id})
    assert rec_res.status_code == 200, rec_res.text
    
    print("7. Copilot Chat...")
    chat_res = client.post("/copilot/chat", json={"message": "What are her strengths?", "candidate_id": candidate_id, "role_id": role_id})
    assert chat_res.status_code == 200, chat_res.text
    
    print("8. Draft Email...")
    draft_res = client.post("/copilot/draft-email", json={"role_id": role_id, "candidate_id": candidate_id})
    assert draft_res.status_code == 200, draft_res.text
    
    print("9. Export Rankings...")
    exp2_res = client.post("/export-rankings", json={"role_id": role_id})
    assert exp2_res.status_code == 200, exp2_res.text
    
    print("10. Graph Build...")
    graph_res = client.post("/build-graph", json={"role_id": role_id, "candidate_ids": [candidate_id]})
    assert graph_res.status_code == 200, graph_res.text
    
    print("E2E workflows passed successfully!")

if __name__ == "__main__":
    run_e2e()
