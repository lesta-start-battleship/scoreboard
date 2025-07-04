from sqlalchemy.ext.asyncio.session import AsyncSession

from broker.schemas.user.new_user import NewUserDTO


class UserRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def create_user(self, user_data: NewUserDTO):
        pass