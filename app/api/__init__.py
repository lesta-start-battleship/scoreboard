from fastapi import APIRouter
from . import user
from . import guild
from . import health

router = APIRouter()
router.include_router(user.router)
router.include_router(guild.router)
router.include_router(health.router)