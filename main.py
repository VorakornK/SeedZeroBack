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

@app.get('/todo/{name}')
async def get_todo(name: str) -> Task:
  task = await Task.find_one({"name": name})
  return task

@app.post("/create_todo")
async def create_task(task_body: TaskBody) -> Task:
  task = Task(**task_body.model_dump())
  await task.insert()
  return task

@app.delete("/delete_todo/{name}")
async def delete_task(name: str):
  del_task = Task.find({"name": name})
  await del_task.delete()

@app.patch("/update_task/{name}")
async def update_task(name: str, new_task: TaskBody):
  task = await Task.find_one({"name": name})
  task.name = new_task.name if new_task.name != None else name
  task.finished = new_task.finished
  await task.save()


  
