from pydantic import BaseModel

from broker.schemas.user.currencies import Currencies


class CurrencyChangeDTO(BaseModel):
    id: int
    currencies: Currencies