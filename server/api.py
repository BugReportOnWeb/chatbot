from fastapi import FastAPI
from pydantic import BaseModel
from controller.main import get_response

app = FastAPI()

class UserInput(BaseModel):
    msg: str

@app.post('/')
def root(req: UserInput):
    res = get_response(req.msg)
    return res

