from sqlalchemy import(
    String,
    Column, 
    ForeignKey,
    DateTime,
    DECIMAL, 
    Enum,
    UUID
)
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from database import Base
import uuid
import enum

class SalesStatus(str, enum.Enum):
    COMPLETED = "completed"
    CANCELLED = "cancelled"
    REFUNDED = "refunded"



class Sale(Base):
    __tablename__="sales"
    
    
    sale_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, autoincrement=False)
    customer_id=Column(UUID(as_uuid=True), ForeignKey("customers.customer_id"), nullable=True)
    user_id= Column(UUID(as_uuid=True), ForeignKey("users.user_id"), nullable=True)
    
    sale_date=Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    subtotal=Column(DECIMAL(10,2), nullable=False)
    tax_amount=Column(DECIMAL(10,2), nullable=False)
    discount_amount=Column(DECIMAL(10,2), nullable=True)
    total_amount=Column(DECIMAL(10,2), nullable=False)
    status=Column(Enum(SalesStatus, name="sale_satus_enum"), nullable=False)
    
    
    user = relationship("User", back_populates="sales")
    customer=relationship("Customer", back_populates="sale")
    receipt = relationship("Receipt", back_populates="sale", uselist=False)
    sale_items = relationship("SaleItem", back_populates="sale")
    