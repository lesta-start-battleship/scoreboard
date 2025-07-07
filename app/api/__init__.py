from . import user
from . import guild

from app import app

app.include_router(user.router)
app.include_router(guild.router)