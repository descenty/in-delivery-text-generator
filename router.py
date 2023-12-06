from fastapi import APIRouter
from rabbit import rabbit_router

router = APIRouter(prefix="/api/v1")

router.include_router(rabbit_router)
