from sqlalchemy import Column, Integer, DECIMAL, DateTime, ForeignKey, Enum
from app.core.database import Base

class Prediction(Base):
    __tablename__ = "predictions"

    id = Column(Integer, primary_key=True, index=True)
    asset_id = Column(Integer, ForeignKey("assets.id"), nullable=False)
    timestamp = Column(DateTime, nullable=False)
    predicted = Column(DECIMAL(18,6))
    confidence = Column(DECIMAL(10,4))
    signall = Column(Enum('BUY', 'HOLD', 'SELL', name='prediction_signall'))
