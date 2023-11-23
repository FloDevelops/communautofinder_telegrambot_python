from fastapi import APIRouter

from .users import router as users

router = APIRouter(
    prefix='/api',
    tags=['api']
)

router.include_router(users.router)