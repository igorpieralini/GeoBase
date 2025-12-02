from pydantic import BaseModel
from typing import Optional

class AssetBase(BaseModel):
    symbol: str
    name: Optional[str] = None
    type: str

class AssetCreate(AssetBase):
    pass

class AssetRead(AssetBase):
    id: int

    class Config:
        orm_mode = True
