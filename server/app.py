#!/usr/bin/env python3

from dotenv import load_dotenv
from chatbot import create_app

import uvicorn
import os

load_dotenv()
HOST_ADDRESS = '0.0.0.0'
SERVER_PORT = int(os.getenv("SERVER_PORT"))

if __name__ == '__main__':
    app = create_app()
    uvicorn.run(app, host=HOST_ADDRESS, port=SERVER_PORT)

