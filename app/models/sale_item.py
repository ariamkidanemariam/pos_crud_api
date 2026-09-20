from sqlalchemy import(
    String,
    Column,
    Integer,
    DECIMAL,
    ForeignKey,
    UUID
)
import uuid
from sqlalchemy.orm import relationship
from database import Base

class SaleItem(Base):
    __tablename__= "sale_items"
    
    
    sale_item_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, autoincrement=False)
    sale_id= Column(UUID(as_uuid=True), ForeignKey("sales.sale_id"), nullable=True)
    product_id= Column(UUID(as_uuid= True), ForeignKey("products.product_id"), nullable=True)
    quantity=Column(Integer, nullable=False)
    unit_price= Column(DECIMAL(10,2), nullable=False)
    discount_amount= Column(DECIMAL(10,2), nullable=True)
    total_price=Column(DECIMAL(10,2), nullable=False)
    
    
    sale = relationship("Sale", back_populates="sale_items")
    product=relationship("Product", back_populates="sale_items")
    
    