from datetime import datetime
from app.models.sale import SalesStatus
from decimal import Decimal
from uuid import UUID
from typing import Optional
from pydantic import BaseModel, ConfigDict

class SalesBase(BaseModel):
    customer_id: UUID
    user_id: UUID
    sale_date: datetime
    subtotal: Decimal
    tax_amount: Decimal
    discount_amount: Optional [Decimal]= None
    total_amount: Decimal 
    status: SalesStatus
    
class SalesCreate(SalesBase):
    pass

class SalesUpdate(BaseModel):
        customer_id: UUID
        user_id: UUID
        sale_date: Optional [datetime] =None
        subtotal: Optional [Decimal]= None
        tax_amount: Optional [Decimal]= None
        discount_amount: Optional [Decimal]= None
        total_amount: Optional [Decimal]= None
        status: Optional [SalesStatus] =None
        
class SalesRead(SalesBase):
    model_config=ConfigDict(from_attributes=True)
    
    sale_id: UUID
    sale_date: datetime