from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Optional

app = FastAPI(title="Task Manager", version="1.0.0")

class Task(BaseModel):
    id: Optional[int] = None
    title: str
    completed: bool = False
    priority: str = "medium"

tasks = [
    Task(id=1, title="Set up project", completed=True, priority="high"),
    Task(id=2, title="Write tests", completed=False, priority="medium"),
]
next_id = 3

@app.get("/")
def root():
    return {"message": "Task Manager API", "docs": "/docs"}

@app.get("/tasks", response_model=List[Task])
def list_t():
    return tasks

@app.get("/tasks/{tid}", response_model=Task)
def get_t(tid: int):
    t = next((x for x in tasks if x.id == tid), None)
    if not t:
        raise HTTPException(404, "Not found")
    return t

@app.post("/tasks", response_model=Task, status_code=201)
def create_t(task: Task):
    global next_id
    task.id = next_id
    next_id += 1
    tasks.append(task)
    return task

@app.patch("/tasks/{tid}")
def update_t(tid: int, updates: dict):
    t = next((x for x in tasks if x.id == tid), None)
    if not t:
        raise HTTPException(404, "Not found")
    for k, v in updates.items():
        setattr(t, k, v)
    return t

@app.delete("/tasks/{tid}", status_code=204)
def delete_t(tid: int):
    global tasks
    tasks = [x for x in tasks if x.id != tid]

@app.get("/health")
def health():
    return {"status": "ok", "count": len(tasks)}