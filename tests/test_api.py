from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_health(monkeypatch):
    monkeypatch.delenv("OPENAI_API_KEY", raising=False)
    monkeypatch.delenv("OPENAI_MODEL", raising=False)
    body = client.get("/health").json()
    assert body["status"] == "ok"
    assert body["ai_mode"] == "reglas"


def test_analyze_text():
    r = client.post("/analyze-text", json={"text": "Hola mundo. Esto es una prueba."})
    assert r.status_code == 200
    assert r.json()["sentences"] == 2


def test_validate_prompt_good():
    p = "Eres un analista. Resume este informe en formato de lista, máximo 100 palabras."
    r = client.post("/validate-prompt", json={"prompt": p})
    assert r.json()["is_valid"] is True and r.json()["score"] == 100


def test_validate_prompt_bad():
    r = client.post("/validate-prompt", json={"prompt": "hola"})
    assert r.json()["is_valid"] is False


def test_empty_text_rejected():
    assert client.post("/analyze-text", json={"text": ""}).status_code == 422


def test_prompt_too_long_rejected():
    assert client.post("/validate-prompt", json={"prompt": "a" * 5001}).status_code == 422


def test_skills_listed():
    names = [s["name"] for s in client.get("/skills").json()]
    assert "prompt-validator" in names


def test_views_are_served():
    assert client.get("/").status_code == 200
    for page in ("escribir", "evaluacion", "mejorado"):
        r = client.get(f"/views/{page}.html")
        assert r.status_code == 200 and "Prompt" in r.text
    assert client.get("/static/app.js").status_code == 200
