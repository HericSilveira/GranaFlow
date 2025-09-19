from fastapi import FastAPI, Response
from threading import Thread
import urllib.request as request
import uvicorn, time

app = FastAPI()

@app.get("/")
async def home():
    return Response()

def keepAlive():
    while True:
        with request.urlopen("https://granaflow-c6wo.onrender.com/") as response:
            ...
        time.sleep(60)

if __name__ == "__main__":
    uvicorn.run(app="main:app", host='0.0.0.0', port=8000)