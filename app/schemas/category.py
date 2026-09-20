from typing import Optional
from pydantic import BaseModel, ConfigDict
from uuid import UUID

class CategoryBase(BaseModel):
    name : str
    description: Optional[str]= None 
    is_active: Optional[bool] = None
    
    

class CategoryCreate(CategoryBase):
    pass

class CategoryUpdate(BaseModel):
    name : Optional[str]= None 
    description: Optional[str]= None 
    is_active: Optional[bool] = True
     
    

class CategoryRead(CategoryBase):
    model_config = ConfigDict(from_attributes=True)

    category_id: UUID