from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from dotenv import load_dotenv

from controller.main import get_response

import os
import uvicorn

load_dotenv()
HOST_ADDRESS = '0.0.0.0'
NETWORK_ADDRESS = os.getenv("NETWORK_ADDRESS")
SERVER_PORT = int(os.getenv("SERVER_PORT"))
CLIENT_PORT = int(os.getenv("CLIENT_PORT"))

app = FastAPI()

origins = [f"{NETWORK_ADDRESS}:{CLIENT_PORT}"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class UserInput(BaseModel):
    msg: str

@app.post('/')
def root(req: UserInput):
    res = get_response(req.msg)
    return res

if __name__ == '__main__':
    uvicorn.run(app, host=HOST_ADDRESS, port=SERVER_PORT)

