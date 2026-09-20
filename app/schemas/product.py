from datetime import datetime
from decimal import Decimal
from typing import Optional
from uuid import UUID
from pydantic import BaseModel, ConfigDict

class ProductBase (BaseModel):
    name:str
    price:Decimal
    quantity:int
    category_id: Optional[UUID] =None
    supplier_id: Optional[UUID] =None
    barcode: Optional[str]= None
    is_active: Optional [bool]=None
    
class ProductCreate (ProductBase):
    pass

class ProductUpdate(BaseModel):
    name:Optional[str]= None
    price: Optional[Decimal] =None
    quantity:Optional[int] =None
    category_id: Optional[UUID] =None
    supplier_id: Optional[UUID] =None
    barcode: Optional[str]= None
    
class   ProductRead(ProductBase):
    model_config=ConfigDict(from_attributes=True)
    
    product_id:UUID
    created_at:datetime