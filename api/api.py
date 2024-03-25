from fastapi import FastAPI
import platform
import sqlite3
app = FastAPI()

# Routes

@app.get("/") 
def read_root():
    values = [
        {"Hello": "World"},
        {"OS": platform.platform()},
        {"Processors": platform.processor()},
        {"System": platform.system()},
        {"Python Version": platform.python_version()}
    ]
    return values

@app.get("/weekly_tasks")
def read_weekly_tasks():
    conn = sqlite3.connect('../db/tasks.db')
    c = conn.cursor()
    c.execute('SELECT * FROM weekly_tasks')
    tasks = c.fetchall()
    conn.close()
    return tasks

@app.get("/tasks")
def read_all_tasks():
    conn = sqlite3.connect('../db/tasks.db')
    c = conn.cursor()
    c.execute('SELECT * FROM all_tasks')
    tasks = c.fetchall()
    conn.close()
    return tasks

@app.get("/tasks/{task_id}")
def read_task(task_id: str):
    conn = sqlite3.connect('../db/tasks.db')
    c = conn.cursor()
    c.execute('SELECT * FROM all_tasks WHERE id = ?', (task_id,))
    task = c.fetchone()
    conn.close()
    return task

# Update task status to completed
@app.get("/tasks/complete/{task_id}")
def complete_task(task_id: str):
    conn = sqlite3.connect('../db/tasks.db')
    c = conn.cursor()
    c.execute('UPDATE all_tasks SET status = 1 WHERE id = ?', (task_id,))
    conn.commit()
    conn.close()
    return {"message": "Task marked as complete"}

# Update task status to incomplete
@app.get("/tasks/incomplete/{task_id}")
def incomplete_task(task_id: str):
    conn = sqlite3.connect('../db/tasks.db')
    c = conn.cursor()
    c.execute('UPDATE all_tasks SET status = 0 WHERE id = ?', (task_id,))
    conn.commit()
    conn.close()
    return {"message": "Task marked as incomplete"}

