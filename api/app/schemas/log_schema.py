from pydantic import BaseModel
from datetime import datetime

class LogSchema(BaseModel):
    level: str
    message: str
    timestamp: datetime
