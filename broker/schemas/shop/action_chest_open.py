from pydantic import BaseModel


class ActionChestOpenDTO(BaseModel):
    user_id: int
    promo: int
    exp: int
