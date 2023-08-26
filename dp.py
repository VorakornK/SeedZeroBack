from beanie import Document
from typing import Optional

class Task(Document):
    name: Optional[str] = None
    finished: bool = False