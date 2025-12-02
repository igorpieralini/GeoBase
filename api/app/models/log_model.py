from sqlalchemy import Column, Integer, DateTime, Enum, Text, String
from app.core.database import Base

class Log(Base):
    __tablename__ = "logs"

    id = Column(Integer, primary_key=True, index=True)
    timestamp = Column(DateTime, nullable=False)
    level = Column(Enum('INFO','WARN','ERROR', name='log_level'))
    message = Column(Text)
    module = Column(String(50))
