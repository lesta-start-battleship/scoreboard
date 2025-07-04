from sqlalchemy.ext.asyncio.session import AsyncSession


class UserRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def create_user(self, *, user_id: int, username: str, email: str, gold: int, guild_rage: int):
        pass

    async def update_username(self, *, user_id: int, username: str):
        pass
