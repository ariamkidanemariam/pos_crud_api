from datetime import datetime
from pydantic import BaseModel, ConfigDict
from app.models.receipt import ReceiptType
from typing import Optional
from uuid import UUID

class ReceiptBase(BaseModel):
    sale_id: UUID
    receipt_number: str
    receipt_type: ReceiptType
    receipt_data: str
    

class ReceiptCreate(ReceiptBase):
    pass

class ReceiptUpdate(BaseModel):
    receipt_number: Optional[str]= None
    receipt_type: Optional [ReceiptType] = None
    receipt_data: Optional[str]= None

class ReceiptRead(ReceiptBase):
    model_config = ConfigDict(from_attributes=True)

    receipt_id: UUID
    generated_at: datetime