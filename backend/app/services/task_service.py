from datetime import datetime

from app.database import get_connection


class TaskService:
    @staticmethod
    def list_tasks() -> list[dict]:
        with get_connection() as conn:
            rows = conn.execute(
                "SELECT * FROM tasks ORDER BY CASE priority WHEN 'high' THEN 0 WHEN 'medium' THEN 1 ELSE 2 END, created_at ASC"
            ).fetchall()
            return [dict(row) for row in rows]

    @staticmethod
    def create_task(title: str, description: str, priority: str) -> dict:
        now = datetime.utcnow().isoformat()
        priority_value = priority.lower()
        with get_connection() as conn:
            cursor = conn.execute(
                """
                INSERT INTO tasks (title, description, priority, completed, created_at, updated_at)
                VALUES (?, ?, ?, ?, ?, ?)
                """,
                (title, description, priority_value, 0, now, now),
            )
            task_id = cursor.lastrowid
            row = conn.execute("SELECT * FROM tasks WHERE id = ?", (task_id,)).fetchone()
            return dict(row)

    @staticmethod
    def toggle_complete(task_id: int) -> dict:
        with get_connection() as conn:
            row = conn.execute("SELECT * FROM tasks WHERE id = ?", (task_id,)).fetchone()
            if not row:
                raise ValueError("Task not found")
            completed = 0 if dict(row)["completed"] else 1
            conn.execute(
                "UPDATE tasks SET completed = ?, updated_at = ? WHERE id = ?",
                (completed, datetime.utcnow().isoformat(), task_id),
            )
            updated = conn.execute("SELECT * FROM tasks WHERE id = ?", (task_id,)).fetchone()
            updated_dict = dict(updated)
            updated_dict["completed"] = bool(updated_dict["completed"])
            return updated_dict

    @staticmethod
    def delete_task(task_id: int) -> None:
        with get_connection() as conn:
            conn.execute("DELETE FROM tasks WHERE id = ?", (task_id,))

    @staticmethod
    def update_task(task_id: int, title: str, description: str, priority: str) -> dict:
        with get_connection() as conn:
            row = conn.execute("SELECT * FROM tasks WHERE id = ?", (task_id,)).fetchone()
            if not row:
                raise ValueError("Task not found")
            conn.execute(
                "UPDATE tasks SET title = ?, description = ?, priority = ?, updated_at = ? WHERE id = ?",
                (title, description, priority.lower(), datetime.utcnow().isoformat(), task_id),
            )
            updated = conn.execute("SELECT * FROM tasks WHERE id = ?", (task_id,)).fetchone()
            return dict(updated)
