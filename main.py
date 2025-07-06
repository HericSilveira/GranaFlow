from fastapi import FastAPI
from fastapi.requests import Request
from fastapi.responses import Response
import uvicorn, Utils, os

app = FastAPI()

@app.route("/")
async def Login(request: Request):
    return Response()