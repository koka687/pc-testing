import json
import sqlite3

import pytest

from app import create_app, export_tasks, init_db


@pytest.fixture
def resources(tmp_path):
    db_path = tmp_path / "tasks.db"
    export_path = tmp_path / "tasks.json"
    app = create_app(db_path, export_path)
    return app.test_client(), db_path, export_path


def test_create_task(resources):
    client, db_path, export_path = resources

    response = client.post("/tasks", json={"title": "Вивчити pytest"})

    assert response.status_code == 201
    assert response.get_json()["title"] == "Вивчити pytest"
    with sqlite3.connect(db_path) as connection:
        row = connection.execute("SELECT title FROM tasks").fetchone()
    assert row == ("Вивчити pytest",)
    assert json.loads(export_path.read_text(encoding="utf-8"))[0]["title"] == "Вивчити pytest"


def test_get_tasks(resources):
    client, _, _ = resources
    client.post("/tasks", json={"title": "Перше завдання"})
    client.post("/tasks", json={"title": "Друге завдання"})

    response = client.get("/tasks")

    assert response.status_code == 200
    assert [task["title"] for task in response.get_json()] == [
        "Перше завдання",
        "Друге завдання",
    ]


def test_tasks_order_in_sqlite(resources):
    client, db_path, _ = resources
    client.post("/tasks", json={"title": "Перше завдання"})
    client.post("/tasks", json={"title": "Друге завдання"})

    with sqlite3.connect(db_path) as connection:
        rows = connection.execute("SELECT id, title FROM tasks ORDER BY id").fetchall()

    assert rows == [(1, "Перше завдання"), (2, "Друге завдання")]


def test_create_task_requires_title(resources):
    client, _, export_path = resources

    response = client.post("/tasks", json={})

    assert response.status_code == 400
    assert response.get_json() == {"error": "Поле title є обов'язковим"}
    assert not export_path.exists()


def test_export_empty_list_and_corrupted_json(tmp_path):
    db_path = tmp_path / "empty.db"
    export_path = tmp_path / "tasks.json"
    init_db(db_path)

    export_tasks(db_path, export_path)
    assert json.loads(export_path.read_text(encoding="utf-8")) == []

    export_path.write_text("{broken_json:", encoding="utf-8")
    with pytest.raises(json.JSONDecodeError):
        json.loads(export_path.read_text(encoding="utf-8"))

    export_tasks(db_path, export_path)
    assert json.loads(export_path.read_text(encoding="utf-8")) == []


def test_delete_task(resources):
    client, db_path, export_path = resources
    first = client.post("/tasks", json={"title": "Завдання 1"}).get_json()
    second = client.post("/tasks", json={"title": "Завдання 2"}).get_json()

    response = client.delete(f"/tasks/{first['id']}")

    assert response.status_code == 200
    assert response.get_json() == {"deleted_id": first["id"]}

    with sqlite3.connect(db_path) as connection:
        rows = connection.execute("SELECT id, title FROM tasks ORDER BY id").fetchall()
    assert rows == [(second["id"], "Завдання 2")]

    exported = json.loads(export_path.read_text(encoding="utf-8"))
    assert exported == [{"id": second["id"], "title": "Завдання 2"}]

    not_found = client.delete("/tasks/999")
    assert not_found.status_code == 404