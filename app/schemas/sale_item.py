from uuid import UUID
from decimal import Decimal
from pydantic import BaseModel, ConfigDict
from typing import Optional

class SaleItemBase(BaseModel):
    sale_id: UUID
    product_id: UUID
    quantity: int
    unit_price: Decimal
    discount_amount: Optional [Decimal]= None
    total_price: Decimal
    

class SaleItemCreate(SaleItemBase):
    pass

class SaleItemUpdate(BaseModel):
    quantity: Optional [int] = None
    unit_price: Optional [Decimal]= None
    discount_amount: Optional [Decimal]= None
    total_price: Optional [Decimal]= None
    

class SaleItemRead(SaleItemBase):
    model_config = ConfigDict(from_attributes=True)

    sale_item_id: UUID