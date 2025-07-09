from pydantic import BaseModel


class CurrencyChangeDTO(BaseModel):
    user_id: int
    gold: int
