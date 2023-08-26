from pydantic import BaseModel
from typing import Optional

class TaskBody(BaseModel):
    name: Optional[str] = None
    finished: bool = False

