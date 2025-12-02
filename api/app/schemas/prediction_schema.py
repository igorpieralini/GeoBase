from pydantic import BaseModel
from datetime import datetime

class PredictionSchema(BaseModel):
    symbol: str
    predicted_price: float
    timestamp: datetime
