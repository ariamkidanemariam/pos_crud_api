from sqlalchemy import(
    String,
    Column, 
    ForeignKey,
    DateTime,
    Text,
    Enum,
    UUID
)
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from database import Base
import uuid
import enum

class ReceiptType(str, enum.Enum):
    SALES_RECIEPT="sales_receipt"
    RETURN_TICKET = "return_ticket"



class Receipt(Base):
    __tablename__="receipts"
    
    receipt_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, autoincrement=False)
    sale_id= Column(UUID(as_uuid= True), ForeignKey("sales.sale_id"), nullable=True)
    receipt_number=Column(String(50), nullable=False, unique=True)
    generated_at=Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    receipt_data= Column(Text, nullable=False)
    type=Column(Enum(ReceiptType, name="receipt_type_enum"), nullable=False)
    
    
    sale = relationship("Sale", back_populates="receipt")   
    