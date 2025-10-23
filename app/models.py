# app/models.py
from sqlalchemy import Column, Integer, Numeric, TIMESTAMP, BigInteger, String
from .db import Base

class TickerData(Base):
    __tablename__ = "ticker_data"

    id = Column(Integer, primary_key=True, index=True)
    datetime = Column(TIMESTAMP, nullable=False, index=True)
    open = Column(Numeric(18,4), nullable=False)
    high = Column(Numeric(18,4), nullable=False)
    low = Column(Numeric(18,4), nullable=False)
    close = Column(Numeric(18,4), nullable=False)
    volume = Column(BigInteger, nullable=False)
    instrument = Column(String(64), nullable=False, default="HINDALCO")
