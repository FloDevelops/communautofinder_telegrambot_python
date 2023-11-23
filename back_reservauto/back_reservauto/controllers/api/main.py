from fastapi import APIRouter

from .users import router as users
from .searches import router as searches

router = APIRouter(
    prefix='/api',
    tags=['api']
)

router.include_router(users.router)
router.include_router(searches.router)