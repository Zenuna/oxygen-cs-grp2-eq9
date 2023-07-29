from database import Base
from sqlalchemy import (
    Column,
    Integer,
    String,
    Double,
)
from datetime import datetime


class OxygenData(Base):
    __tablename__ = "OxygenData"
    __table_args__ = {"extend_existing": True}
    id = Column(Integer(), primary_key=True)
    timestamp = Column(String(255))
    temp = Column(Double())
    message = Column(String(255))

    def to_json(self):
        return {
            "timestamp": self.timestamp.strftime("%Y-%m-%d %H:%M:%S")
            if isinstance(self.timestamp, datetime)
            else None,
            "temp": self.temp,
            "message": self.message,
        }
