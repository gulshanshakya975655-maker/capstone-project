from algorithms import insertion_sort, binary_search, linear_search
import time
from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from sqlalchemy import func

import models
import schemas
from database import engine, get_db

models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="TaskFlow API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://127.0.0.1:5500", "http://localhost:5500"],
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],
    allow_headers=["Content-Type", "Authorization"],
)


@app.middleware("http")
async def log_requests(request, call_next):
    start_time = time.time()
    response = await call_next(request)
    duration_ms = (time.time() - start_time) * 1000
    print(f"[LOG] {request.method} {request.url.path} - {duration_ms:.2f}ms")
    return response


@app.post("/users", response_model=schemas.UserOut, status_code=201)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    db_user = models.User(name=user.name, email=user.email)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


@app.get("/users", response_model=list[schemas.UserOut])
def list_users(db: Session = Depends(get_db)):
    return db.query(models.User).all()


@app.post("/projects", response_model=schemas.ProjectOut, status_code=201)
def create_project(project: schemas.ProjectCreate, db: Session = Depends(get_db)):
    owner = db.query(models.User).filter(models.User.id == project.owner_id).first()
    if not owner:
        raise HTTPException(status_code=404, detail="User nahi mila")

    db_project = models.Project(name=project.name, owner_id=project.owner_id)
    db.add(db_project)
    db.commit()
    db.refresh(db_project)
    return db_project


@app.get("/projects", response_model=list[schemas.ProjectOut])
def list_projects(db: Session = Depends(get_db)):
    return db.query(models.Project).all()


@app.post("/tasks", response_model=schemas.TaskOut, status_code=201)
def create_task(task: schemas.TaskCreate, db: Session = Depends(get_db)):
    project = db.query(models.Project).filter(models.Project.id == task.project_id).first()
    if not project:
        raise HTTPException(status_code=404, detail="Project nahi mila")

    db_task = models.Task(
        title=task.title,
        priority=task.priority,
        due_date=task.due_date,
        project_id=task.project_id,
    )
    db.add(db_task)
    db.commit()
    db.refresh(db_task)
    return db_task


@app.get("/tasks", response_model=list[schemas.TaskOut])
def list_tasks(sort: str = None, db: Session = Depends(get_db)):
    """
    Agar ?sort=priority ya ?sort=due_date diya gaya hai,
    to hum apna khud ka insertion_sort() use karke sort karte hain
    (Python ka built-in sorted() NAHI use kar rahe).
    """
    tasks = db.query(models.Task).all()

    task_dicts = [
        {
            "id": t.id,
            "title": t.title,
            "priority": t.priority,
            "due_date": t.due_date,
            "project_id": t.project_id,
        }
        for t in tasks
    ]

    if sort == "priority":
        priority_rank = {"low": 1, "medium": 2, "high": 3}
        for d in task_dicts:
            d["priority_rank"] = priority_rank.get(d["priority"], 0)

        insertion_sort(task_dicts, "priority_rank")

        for d in task_dicts:
            d.pop("priority_rank")
        return task_dicts

    elif sort == "due_date":
        for d in task_dicts:
            if d["due_date"] is None:
                d["due_date"] = ""

        insertion_sort(task_dicts, "due_date")
        return task_dicts

    return task_dicts


@app.get("/tasks/search")
def search_task(title: str, algo: str = "binary", db: Session = Depends(get_db)):
    """
    Task ko exact title se dhoondta hai.
    algo=binary (default) -> pehle sort karta hai, phir binary_search
    algo=linear -> bina sort kiye, seedha linear_search
    """
    tasks = db.query(models.Task).all()

    index_list = [{"id": t.id, "title": t.title} for t in tasks]

    if algo == "linear":
        found_index = linear_search(index_list, title, "title")
    else:
        insertion_sort(index_list, "title")
        found_index = binary_search(index_list, title, "title")

    if found_index == -1:
        raise HTTPException(status_code=404, detail="Task nahi mila")

    matched_id = index_list[found_index]["id"]
    task = db.query(models.Task).filter(models.Task.id == matched_id).first()
    return task


@app.get("/tasks/{task_id}", response_model=schemas.TaskOut)
def get_task(task_id: int, db: Session = Depends(get_db)):
    task = db.query(models.Task).filter(models.Task.id == task_id).first()
    if not task:
        raise HTTPException(status_code=404, detail="Task nahi mila")
    return task


@app.put("/tasks/{task_id}", response_model=schemas.TaskOut)
def update_task(task_id: int, updated: schemas.TaskUpdate, db: Session = Depends(get_db)):
    task = db.query(models.Task).filter(models.Task.id == task_id).first()
    if not task:
        raise HTTPException(status_code=404, detail="Task nahi mila")

    if updated.title is not None:
        task.title = updated.title
    if updated.priority is not None:
        task.priority = updated.priority
    if updated.due_date is not None:
        task.due_date = updated.due_date

    db.commit()
    db.refresh(task)
    return task


@app.delete("/tasks/{task_id}", status_code=200)
def delete_task(task_id: int, db: Session = Depends(get_db)):
    task = db.query(models.Task).filter(models.Task.id == task_id).first()
    if not task:
        raise HTTPException(status_code=404, detail="Task nahi mila")

    db.delete(task)
    db.commit()
    return {"message": "Task delete ho gaya", "id": task_id}


@app.get("/projects/stats", response_model=list[schemas.ProjectStats])
def project_statistics(db: Session = Depends(get_db)):
    results = (
        db.query(
            models.Project.id.label("project_id"),
            models.Project.name.label("project_name"),
            func.count(models.Task.id).label("total_tasks"),
        )
        .outerjoin(models.Task, models.Task.project_id == models.Project.id)
        .group_by(models.Project.id)
        .all()
    )
    return results