from fastapi import APIRouter

router = APIRouter(
    prefix="/user",
    tags=["Routes", "Rotas"],
)

@router.post("/registration")
async def registration():
    raise NotImplementedError

@router.post("/login")
async def login():
    raise NotImplementedError