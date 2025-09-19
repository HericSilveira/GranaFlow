from fastapi import FastAPI, Response
from threading import Thread
import urllib.request as request
import uvicorn, time

app = FastAPI()

if __name__ == "__main__":
    uvicorn.run(app="main:app", host='0.0.0.0', port=8000)