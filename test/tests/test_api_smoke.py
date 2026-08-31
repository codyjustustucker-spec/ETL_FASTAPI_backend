from fastapi.testclient import TestClient
from lso.main import app


def test_healthz():
    with TestClient(app) as client:
        r = client.get("/healthz")
        assert r.status_code == 200
        assert r.json()["ok"] is True


def test_create_and_list_system():
    with TestClient(app) as client:
        r = client.post("/systems", json={"name": "smoke_sys"})
        assert r.status_code == 201
        sys_id = r.json()["id"]

        r = client.get("/systems")
        assert r.status_code == 200
        assert any(s["id"] == sys_id for s in r.json())
