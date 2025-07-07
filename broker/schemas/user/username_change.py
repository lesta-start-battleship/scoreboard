from pydantic import BaseModel


class UsernameChangeDTO(BaseModel):
    user_id: int
    username: str
