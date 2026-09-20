from datetime import datetime
from typing import Optional
from uuid import UUID
from pydantic import ConfigDict, BaseModel

class SupplierBase( BaseModel):
    company_name: str
    contact_name: Optional [str]= None
    email: Optional[str] = "user@gmail.com"
    supplier_phone: Optional [str]= None
    address: Optional [str]= None
    is_active: Optional [bool] = None
    
class SupplierCreate(SupplierBase):
    pass

class SupplierUpdate( BaseModel):
    company_name: Optional [str]= None
    contact_name: Optional [str]= None
    email:Optional [str]= None
    supplier_phone: Optional [str]= None
    address: Optional [str]= None
    is_active: Optional [bool] = True
    
class SupplierRead(SupplierBase):
    model_config = ConfigDict(from_attributes=True)
    
    supplier_id: UUID