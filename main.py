from fastapi import FastAPI
from Routes import routers

app = FastAPI()

for router in routers:
    app.include_router(router)

if __name__ == "__main__":
    import uvicorn, os
    uvicorn.run(app, host=os.getenv("HOST", "0.0.0.0"), port=int(os.getenv("PORT", 8000)))