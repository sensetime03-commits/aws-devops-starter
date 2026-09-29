import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from app import app  # noqa: E402


def test_health():
    client = app.test_client()
    res = client.get("/health")
    assert res.status_code == 200
    assert res.get_json()["status"] == "ok"


def test_add_and_list_notes():
    client = app.test_client()
    res = client.post("/notes", json={"text": "learn devops"})
    assert res.status_code == 201
    res = client.get("/notes")
    assert any(n["text"] == "learn devops" for n in res.get_json())


def test_add_note_without_text():
    client = app.test_client()
    res = client.post("/notes", json={})
    assert res.status_code == 400
