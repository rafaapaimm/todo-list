from fastapi.testclient import TestClient

from app.main import app


def test_homepage_renders_task_form_and_list():
    client = TestClient(app)
    response = client.get("/")
    assert response.status_code == 200
    assert "Create Task" in response.text
    assert "priority" in response.text.lower()
