from sqlalchemy import Column, Integer, DECIMAL, DateTime, ForeignKey
from app.core.database import Base

class Price(Base):
    __tablename__ = "prices"

    id = Column(Integer, primary_key=True, index=True)
    asset_id = Column(Integer, ForeignKey("assets.id"), nullable=False)
    timestamp = Column(DateTime, nullable=False)
    open = Column(DECIMAL(18,6))
    close = Column(DECIMAL(18,6))
    high = Column(DECIMAL(18,6))
    low = Column(DECIMAL(18,6))
    volume = Column(DECIMAL(18,2))
