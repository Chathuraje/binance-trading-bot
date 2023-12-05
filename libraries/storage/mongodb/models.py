from typing import Optional, Dict
from pydantic import BaseModel

class TakeProfitData(BaseModel):
    orderId: str
    clientOrderId: str
    price: float

class StopLossData(BaseModel):
    orderId: str
    clientOrderId: str
    stopPrice: float

class OrderDB(BaseModel):
    orderId: str
    clientOrderId: str
    time: str
    origType: str
    side: str
    positionSide: str
    origQty: float
    closePrice: float
    stopLoss: Optional[StopLossData]
    takeProfit: Optional[TakeProfitData]
    status: str
    
class ActiveTradeDB(BaseModel):
    tradeOrderId: str
    stopLossOrderId: float
    takeProfitOrderId: float
    tradeID: str