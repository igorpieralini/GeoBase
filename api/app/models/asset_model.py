from sqlalchemy import Column, Integer, String, Enum
from app.core.database import Base

class Asset(Base):
    __tablename__ = "assets"

    id = Column(Integer, primary_key=True, index=True)
    symbol = Column(String(20), nullable=False, unique=True)
    name = Column(String(100))
    type = Column(Enum('stock', 'crypto', name='asset_type'), nullable=False)
