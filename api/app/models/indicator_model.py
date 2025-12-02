from sqlalchemy import Column, Integer, DECIMAL, DateTime, ForeignKey
from app.core.database import Base

class Indicator(Base):
    __tablename__ = "indicators"

    id = Column(Integer, primary_key=True, index=True)
    asset_id = Column(Integer, ForeignKey("assets.id"), nullable=False)
    timestamp = Column(DateTime, nullable=False)
    rsi = Column(DECIMAL(10,4))
    macd = Column(DECIMAL(10,4))
    signall = Column(DECIMAL(10,4))
    ma9 = Column(DECIMAL(10,4))
    ma21 = Column(DECIMAL(10,4))
