from pydantic import BaseModel

class TaskBody(BaseModel):
    name: str
    finished: bool = False

