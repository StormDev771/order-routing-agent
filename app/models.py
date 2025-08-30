from __future__ import annotations
from typing import Any, Dict, List, Optional
from pydantic import BaseModel, Field

class Order(BaseModel):
    OrderID: Optional[str] = Field(default=None)
    CustomerName: Optional[str] = None
    Address: Optional[str] = None
    PaymentStatus: Optional[str] = None
    Priority: Optional[str] = None
    Notes: Optional[str] = None

class ClassifiedOrder(Order):
    Category: str
    Explanation: str

class OrdersResponse(BaseModel):
    results: List[ClassifiedOrder]
    count: int

class EvaluationResult(BaseModel):
    metrics: Dict[str, Any]
    sample_predictions: List[Dict[str, Any]]