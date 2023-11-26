from sqlalchemy import Column, DateTime, Float
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class HistoricalData(Base):
    __tablename__ = 'HistoricalData'

    timestamp = Column(DateTime, primary_key=True)
    open = Column(Float)
    high = Column(Float)
    low = Column(Float)
    close = Column(Float)
    volume = Column(Float)
