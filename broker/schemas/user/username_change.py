from pydantic import BaseModel, Field


class UsernameChangeDTO(BaseModel):
    user_id: int
    name: str = Field(..., alias="username")
