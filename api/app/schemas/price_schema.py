from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class PriceBase(BaseModel):
    timestamp: datetime
    open: Optional[float] = None
    close: Optional[float] = None
    high: Optional[float] = None
    low: Optional[float] = None
    volume: Optional[float] = None

class PriceCreate(PriceBase):
    asset_id: int

class PriceRead(PriceBase):
    id: int
    asset_id: int

    class Config:
        orm_mode = True
