import asyncio, sys

if sys.platform == "win32":
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

from fastapi import FastAPI
from fastapi.requests import Request
from fastapi.responses import Response, JSONResponse
from typing import Any
from Utils.Utils import Database, Criptografia

app = FastAPI()
database = Database()
app.add_event_handler("startup", database.init_pool)


@app.route("/Login")
async def Login(request: Request) -> JSONResponse:
    Connection = await database.get_conn()
    try:
        #Transforma a query em um dicionario python
        Parameters: dict[str, Any] = dict(request.query_params.items())

        if not Parameters:
            return JSONResponse({"Status": "Parametros inválidos ou faltando"}, status_code=400)
                    
        Email: str | None = Parameters.get("Email")
        Password: str | None = Parameters.get("Senha")

        if not Email or not Password:
            return JSONResponse({"Status": "Parametros inválidos ou faltando"}, status_code=400)
        
        Email = Email.lower()

        
        async with Connection.cursor() as Cursor: 
            await Cursor.execute("SELECT id, senha FROM usuarios WHERE email = %s", (Email, ))
            result = await Cursor.fetchone()
        
        if not result:
            return JSONResponse({"Status": "Email ou senha incorretos"}, status_code=400)
        
        if Criptografia().verify_hash(Password, result[1]):
            return JSONResponse({"Status": "Login realizado com sucesso", "UserID": result[0]})
        
        return JSONResponse({"Status": "Email ou senha incorretos"}, status_code=400)
    
    except Exception as Error:
        print(Error)
        return JSONResponse({"Status": "Erro ao realizar o Login"}, status_code=500)
    
    finally:
        await database.release_conn(Connection)

@app.get("/Registration")
async def Registration(request: Request) -> JSONResponse:
    Connection = await database.get_conn()
    try:
        Parameters: dict[str, Any] = dict(request.query_params.items())

        if not Parameters:
            return JSONResponse({"Status": "Parametros inválidos ou faltando"}, status_code=400)
                
        Name: str | None = Parameters.get("Nome")
        Email: str | None = Parameters.get("Email")
        Password: str | None = Parameters.get("Senha")

        if not Name or not Email or not Password:
            return JSONResponse({"Status": "Parametros inválidos ou faltando"}, status_code=400)
        
        Email = Email.lower()
        
        #Primeiro verifica se o email já existe para só então realizar o cadastro isso evita de realizar um hash de senha desnecessario
        async with Connection.cursor() as Cursor:
            await Cursor.execute("SELECT id FROM usuarios WHERE email = %s", (Email, ))
            result = await Cursor.fetchone()
        
            if result:
                return JSONResponse({"Status": "Email ja cadastrado"}, status_code=400)
            
            Password = Criptografia().hash(Password)

            result = await Cursor.execute("INSERT INTO usuarios (nome, email, senha) VALUES (%s, %s, %s) ON CONFLICT (email) DO NOTHING RETURNING id", (Name, Email, Password))
        
        await Connection.commit()
        return JSONResponse({"Status": "Cadastro realizado com sucesso"})
    except Exception as Error:
        print(Error)
        return JSONResponse({"Status": "Erro ao realizar o cadastro"}, status_code=500)
    finally:
        await database.release_conn(Connection)

if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=10000)