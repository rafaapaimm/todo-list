from fastapi import FastAPI, Request, Form
from fastapi.responses import JSONResponse
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


@app.post("/tasks/{task_id}/edit")
def edit_task(
    task_id: int,
    title: str = Form(...),
    description: str = Form(""),
    priority: str = Form("medium"),
):
    payload = TaskCreate(title=title, description=description, priority=priority)
    task = TaskService.update_task(task_id, payload.title, payload.description, payload.normalized_priority)
    return JSONResponse(status_code=200, content=task)


@app.post("/tasks/{task_id}/delete")
def delete_task(task_id: int):
    TaskService.delete_task(task_id)
    return JSONResponse(status_code=200, content={"deleted": True, "id": task_id})
