from pydantic import BaseModel, Field, ConfigDict
from typing import Annotated

from .models import LotStatus


class LotCreate(BaseModel):
    title: str
    description: str
    starting_price: Annotated[float, Field(gt=0)]

class LotRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    title: str
    description: str
    starting_price: float
    status: LotStatus

class BidCreate(BaseModel):
    amount: Annotated[float, Field(gt=0)]

class BidRead(BaseModel):
    id: int
    lot_id: int
    amount: float

    model_config = dict(from_attributes=True)

