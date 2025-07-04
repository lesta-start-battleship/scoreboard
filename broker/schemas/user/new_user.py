from pydantic import BaseModel

from broker.schemas.user.currencies import Currencies


class NewUserDTO(BaseModel):
    id: int
    username: str
    email: str
    currencies: Currencies