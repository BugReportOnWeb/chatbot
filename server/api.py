from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

class UserInput(BaseModel):
    msg: str

@app.post('/')
def root(req: UserInput):
    return req.msg

