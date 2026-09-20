from datetime import datetime
from typing import Optional
from pydantic import BaseModel, ConfigDict
from uuid import UUID
class CustomerBase(BaseModel):
    first_name : str
    last_name : str
    phone_no :Optional[str]= None 
    address :Optional[str]= None 
    is_active : Optional[bool] = None
    
class CustomerCreate(CustomerBase):
    pass

class CustomerUpdate(BaseModel):
        first_name : Optional[str]= None 
        last_name : Optional[str]= None 
        phone_no :Optional[str]= None 
        address :Optional[str]= None 
        is_active: Optional[bool] = True        
class CustomerRead(CustomerBase):
    model_config=ConfigDict(from_attributes=True)
    
    customer_id: UUID
    created_at: datetime
    updated_at : datetime
    