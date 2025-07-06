import psycopg, os, asyncio
from dotenv import load_dotenv
from argon2 import PasswordHasher, profiles, exceptions as argon2_exceptions

load_dotenv()

class Database:

    _conn_queue: asyncio.Queue[psycopg.AsyncConnection]

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
    
    async def release_conn(self, conn: psycopg.AsyncConnection, cursor: list[psycopg.AsyncCursor]|psycopg.AsyncCursor|None = None):
        if cursor:
            if isinstance(cursor, list):
                for cursor in cursor:
                    await cursor.close()
            else:
                await cursor.close()
            
        await self._conn_queue.put(conn)

    async def close_queue(self):
        while not self._conn_queue.empty():
            conn = await self._conn_queue.get()
            await conn.close()
    
class Criptografia:

    hasher = PasswordHasher(
            profiles.RFC_9106_HIGH_MEMORY.time_cost,
            profiles.RFC_9106_HIGH_MEMORY.memory_cost,
            profiles.RFC_9106_HIGH_MEMORY.parallelism,
            profiles.RFC_9106_HIGH_MEMORY.hash_len,
            profiles.RFC_9106_HIGH_MEMORY.salt_len
        )

    def hash(self, password: str) -> str:
        return self.hasher.hash(password)
    
    def verify_hash(self, password: str, hash: str) -> bool:
        try:
            return self.hasher.verify(hash, password)
        except argon2_exceptions.VerifyMismatchError:
            return False
        except Exception as Error:
            print(Error)
            return False