from pydantic import BaseModel

from broker.schemas.user.currencies import Currencies


class NewUserDTO(BaseModel):
    user_id: int
    username: str
    email: str
    currencies: Currencies