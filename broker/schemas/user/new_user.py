from pydantic import BaseModel


class NewUserDTO(BaseModel):
    user_id: int
    username: str
    email: str
    role: str
    gold: int
