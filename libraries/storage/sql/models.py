from sqlalchemy import Column, DateTime, Float, INTEGER
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
class StrategyData(Base):
    __tablename__ = 'StrategyData'

    timestamp = Column(DateTime, primary_key=True)
    close = Column(Float)
    bb_upper = Column(Float)
    bb_lower = Column(Float)
    ema = Column(Float)
    signal = Column(INTEGER)
