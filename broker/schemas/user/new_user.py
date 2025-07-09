from pydantic import BaseModel, Field


class NewUserDTO(BaseModel):
    user_id: int
    name: str = Field(..., alias="username")
    gold: int
