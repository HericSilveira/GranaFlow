import asyncio, sys

if sys.platform == "win32":
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

from fastapi import FastAPI
from fastapi.requests import Request
from fastapi.responses import Response, JSONResponse
from typing import Any
from Utils import Utils

app = FastAPI()
Database = Utils.Database()
app.add_event_handler("startup", Database.init_pool)


@app.route("/")
async def Login(request: Request) -> JSONResponse:
    return JSONResponse({})

@app.get("/Registration")
async def Registration(request: Request) -> JSONResponse:
    print(request.query_params.values())
    Parameters: Any|dict[str, Any] = dict(request.query_params.items())
    if not isinstance(Parameters, dict):
        return JSONResponse({"Status": "Parametros inválidos"}, status_code=400)
    Email, Password = Parameters.get("Email"), Parameters.get("Senha")
    
    Connection = await Database.get_conn()
    result = await Connection.execute("SELECT 1")

    if _ := await result.fetchone():
        print(_)
        await Database.release_conn(Connection)
        return JSONResponse({"Resultado": _[0]})
    
    return JSONResponse({"Status": "Parametros inválidos"}, status_code=400)

if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, 
                host="0.0.0.0", 
                port=10000
                )