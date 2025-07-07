from fastapi import APIRouter
from . import user
from . import guild

router = APIRouter()
router.include_router(user.router)
router.include_router(guild.router)