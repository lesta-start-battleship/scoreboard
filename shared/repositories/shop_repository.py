from sqlalchemy.ext.asyncio.session import AsyncSession


class ShopRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def open_chest(self, user_id: int, exp: int, **kwargs):
        pass
