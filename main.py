from fastapi import FastAPI
from fastapi.requests import Request
from fastapi.responses import Response
import uvicorn, Utils, os

APP = FastAPI()

@APP.route("/")
async def Login(request: Request):
    return Response()

if __name__ == "__main__":
    if PORTA := os.getenv("PORTA"):
        uvicorn.run(APP, host="0.0.0.0", port = int(PORTA))