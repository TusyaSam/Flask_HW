from fastapi import FastAPI, HTTPException
from typing import List
from pydantic import BaseModel


# Необходимо создать API для управления списком задач. 
# Каждая задача должна содержать заголовок и описание. 
# Для каждой задачи должна быть возможность указать статус (выполнена/не выполнена).

# API должен содержать следующие конечные точки:
# — GET /tasks — возвращает список всех задач.
# — GET /tasks/{id} — возвращает задачу с указанным идентификатором.
# — POST /tasks — добавляет новую задачу.
# — PUT /tasks/{id} — обновляет задачу с указанным идентификатором.
# — DELETE /tasks/{id} — удаляет задачу с указанным идентификатором.

# Для каждой конечной точки необходимо проводить валидацию данных запроса и ответа. 
# Для этого использовать библиотеку Pydantic.

class Task(BaseModel):
    id: int
    header: str
    description: str
    done: bool


app = FastAPI()
db = list()



@app.get("/tasks/", response_model=List[Task])
async def get_tasks():
    return db


@app.get("/tasks/{task_id}", response_model=Task)
async def get_task(task_id: int):
    for i in range(len(db)):
        if db[i].id == task_id:
            return db[i]
    raise HTTPException(status_code=404, detail=f'Task {task_id} not found')


@app.post("/tasks/", response_model=Task)
async def add_user(task: Task):
    task.id = len(db) + 1
    db.append(task)
    return task


@app.put("/tasks/{task_id}", response_model=Task)
async def update_task(task_id: int, task: Task):
    task.id = task_id
    for i in range(len(db)):
        if db[i].id == task_id:
            db[i] = task
            return task
    raise HTTPException(status_code=404, detail=f'Task {task_id} not found')


@app.delete("/tasks/{task_id}", response_model=Task)
async def delete_task(task_id: int):
    for i in range(len(db)):
        if db[i].id == task_id:
            task = db[i]
            db.pop(i)
            return task
    raise HTTPException(status_code=404, detail=f'Task {task_id} not found')



if __name__ == '__main__':
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)