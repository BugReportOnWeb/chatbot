from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from controller.main import get_response

import uvicorn

HOST_ADDRESS = '0.0.0.0'
PORT = 8000

app = FastAPI()

class UserInput(BaseModel):
    msg: str

@app.post('/')
def root(req: UserInput):
    res = get_response(req.msg)
    return res

if __name__ == '__main__':
    uvicorn.run(app, host=HOST_ADDRESS, port=PORT)

