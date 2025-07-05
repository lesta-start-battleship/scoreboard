from pydantic import BaseModel


class ActionChestOpenDTO(BaseModel):
    user_id: int
    event: str
    exp: int
