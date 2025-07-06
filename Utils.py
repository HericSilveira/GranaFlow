from dotenv import load_dotenv
import psycopg, os, asyncio, requests

load_dotenv()

class Database:

    _conn_queue: asyncio.Queue[psycopg.AsyncConnection] = asyncio.Queue(10)

    async def init_pool(self):
        for _ in range(self._conn_queue.maxsize):
            conn = await psycopg.AsyncConnection.connect(
                host = os.getenv("HOST"),
                port = os.getenv("PORT"),
                dbname = os.getenv("DATABASE"),
                user = os.getenv("USER"),
                password = os.getenv("PASSWORD")
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

