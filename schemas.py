from pydantic import BaseModel


class STaskADD(BaseModel):
    name: str
    description: str

class STask(STaskADD):
    id: int
    title:str
    description :str

class STaskId(BaseModel):
    ok: bool = True
    task_id :int



class UserLoginSchema(BaseModel):
    username:str
    password:str