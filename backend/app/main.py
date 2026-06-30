from fastapi import FastAPI, Form, HTTPException, Request
from fastapi.responses import JSONResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from app.schemas import TaskCreate
from app.services.task_service import TaskService

app = FastAPI(title="Task List App")
app.mount("/static", StaticFiles(directory="app/static"), name="static")

templates = Jinja2Templates(directory="app/templates")


@app.get("/")
def home(request: Request):
    tasks = TaskService.list_tasks()
    return templates.TemplateResponse(
        request,
        "tasks.html",
        {"tasks": tasks, "error": None},
    )


@app.post("/tasks")
def create_task(
    title: str = Form(...),
    description: str = Form(""),
    priority: str = Form("medium"),
):
    payload = TaskCreate(title=title, description=description, priority=priority)
    task = TaskService.create_task(
        payload.title,
        payload.description,
        payload.normalized_priority,
    )
    return JSONResponse(status_code=200, content=task)


@app.post("/tasks/{task_id}/complete")
def complete_task(task_id: int):
    task = TaskService.toggle_complete(task_id)
    return JSONResponse(status_code=200, content=task)


@app.get("/tasks/{task_id}/edit")
def show_edit_task(request: Request, task_id: int):
    task = TaskService.get_task(task_id)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    return templates.TemplateResponse(
        request,
        "edit_task.html",
        {"task": task, "error": None},
    )


@app.post("/tasks/{task_id}/edit")
def edit_task(
    task_id: int,
    title: str = Form(...),
    description: str = Form(""),
    priority: str = Form("medium"),
):
    payload = TaskCreate(title=title, description=description, priority=priority)
    try:
        TaskService.update_task(task_id, payload.title, payload.description, payload.normalized_priority)
    except ValueError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc
    return RedirectResponse(url="/", status_code=303)


@app.post("/tasks/{task_id}/delete")
def delete_task(task_id: int):
    TaskService.delete_task(task_id)
    return JSONResponse(status_code=200, content={"deleted": True, "id": task_id})
