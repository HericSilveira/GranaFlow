import psycopg, os, asyncio
from dotenv import load_dotenv

load_dotenv()

class Database:

    def __init__(self, MaxSize: int = 1) -> None:
        self._conn_queue = asyncio.Queue(maxsize = MaxSize)

    async def init_pool(self):
        for _ in range(self._conn_queue.maxsize):
            # URL = "postgresql://granaflow_user:X1AfnmUBIerbMZwqMZITO25Ha84Ht7e3@dpg-d1kst2h5pdvs73b8r9bg-a.virginia-postgres.render.com/granaflow"
            port: int|str|None = os.getenv("PORT")
            port = int(port) if port else 5432
            conn = await psycopg.AsyncConnection.connect(
            
                host=os.getenv("HOST"),
                port=port,
                user=os.getenv("USER"),
                password=os.getenv("PASSWORD"),
                dbname=os.getenv("DATABASE")
            )
            await self._conn_queue.put(conn)
    
    async def get_conn(self):
        return await self._conn_queue.get()
    
    async def release_conn(self, conn: psycopg.AsyncConnection):
        await self._conn_queue.put(conn)

    async def close_queue(self):
        while not self._conn_queue.empty():
            conn = await self._conn_queue.get()
            await conn.close()
    
async def main():
    DBs = Database()
    await DBs.init_pool()

    conn = await DBs.get_conn()

    await conn.execute("""CREATE TABLE IF NOT EXISTS usuarios(
                       id SERIAL PRIMARY KEY,
                       nome VARCHAR(64) NOT NULL,
                       email VARCHAR(128) NOT NULL UNIQUE,
                       senha VARCHAR(255) NOT NULL
                       )""")

    await DBs.release_conn(conn)
    await DBs.close_queue()

if __name__ == "__main__":
    print(asyncio.run(main()))