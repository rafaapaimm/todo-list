from fastapi.testclient import TestClient

from app.main import app


def test_create_and_list_tasks():
    client = TestClient(app)
    response = client.post(
        "/tasks",
        data={"title": "Estudar", "description": "Revisar FastAPI", "priority": "high"},
    )
    assert response.status_code == 200

    list_response = client.get("/")
    assert list_response.status_code == 200
    assert "Estudar" in list_response.text
    assert "high" in list_response.text


def test_toggle_complete_and_delete_task():
    client = TestClient(app)
    create_response = client.post(
        "/tasks",
        data={"title": "Lavar roupa", "description": "", "priority": "medium"},
    )
    assert create_response.status_code == 200

    task_id = create_response.json()["id"]
    toggle_response = client.post(f"/tasks/{task_id}/complete")
    assert toggle_response.status_code == 200
    assert toggle_response.json()["completed"] is True

    delete_response = client.post(f"/tasks/{task_id}/delete")
    assert delete_response.status_code == 200


def test_edit_form_renders_and_updates_task():
    client = TestClient(app)
    create_response = client.post(
        "/tasks",
        data={"title": "Comprar pão", "description": "Na padaria", "priority": "medium"},
    )
    assert create_response.status_code == 200

    task_id = create_response.json()["id"]
    edit_page = client.get(f"/tasks/{task_id}/edit")
    assert edit_page.status_code == 200
    assert "Edit Task" in edit_page.text
    assert "Comprar pão" in edit_page.text

    update_response = client.post(
        f"/tasks/{task_id}/edit",
        data={"title": "Comprar pão integral", "description": "Na padaria", "priority": "low"},
        follow_redirects=False,
    )
    assert update_response.status_code == 303

    list_response = client.get("/")
    assert "Comprar pão integral" in list_response.text
