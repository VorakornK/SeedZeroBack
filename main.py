from fastapi import FastAPI
from pydantic import BaseModel
from motor.motor_asyncio import AsyncIOMotorClient
from beanie import init_beanie
from model import TaskBody
from dp import Task
from typing import List
app = FastAPI()


@app.on_event("startup")
async def startup():
  client = AsyncIOMotorClient("mongodb://localhost:27017")
  await init_beanie(database=client.notphoom, document_models=[Task])

@app.get('/todos')
async def get_alltasks() -> List[Task]:
  tasks = await Task.find().to_list()
  return tasks

@app.post("/create_todo")
async def create_task(task_body: TaskBody) -> Task:
  task = Task(**task_body.model_dump())
  await task.insert()
  return task

@app.delete("/delete_todo/{id}")
async def delete_task(id: str):
  del_task = await Task.get(id)
  await del_task.delete()

@app.put("/update_task/{id}")
async def update_task(id: str, new_task: TaskBody):
  task = await Task.get(id)
  task.name = new_task.name
  task.finished = new_task.finished

  await task.save()


  
