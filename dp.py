from beanie import Document

class Task(Document):
    name: str
    finished: bool = False