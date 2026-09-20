from datetime import datetime
from decimal import Decimal
from typing import Optional
from uuid import UUID
from app.models.payment import PaymentMethod, PaymentStatus
from pydantic import BaseModel, ConfigDict


class PaymentBase(BaseModel):
    sale_id: UUID
    payment_method : PaymentMethod
    amount: Decimal
    payment_date: datetime  
    payment_date: datetime
    status: PaymentStatus
    

class PaymentCreate(PaymentBase):
    pass

class PaymentUpdate(BaseModel):
    payment_method : Optional [PaymentMethod] = None
    amount: Optional [Decimal] = None
    payment_date: Optional [datetime] = None
    status: Optional [PaymentStatus] = None
    

class PaymentRead(PaymentBase):
    model_config = ConfigDict(from_attributes=True)
    
    payment_id: UUID
    payment_date: datetime