from sqlalchemy import (
    Boolean, 
    Column,
    DateTime,
    ForeignKey, 
    Integer,
    DECIMAL, 
    String,
    UUID
)

from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
import uuid
from database import Base

class Product(Base):
    __tablename__= "products"
    
    product_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, autoincrement=False)
    name=Column(String, nullable=False)
    price=Column(DECIMAL(10,2), nullable=False)
    quantity= Column(Integer,nullable=False)
    category_id = Column(UUID(as_uuid= True), ForeignKey("categories.category_id"), nullable=True)
    supplier_id = Column(UUID(as_uuid= True), ForeignKey("suppliers.supplier_id"), nullable=True)
    barcode= Column(String, nullable=True)
    is_active=Column(Boolean, nullable=False, default=True)
    created_at=Column(DateTime(timezone=True), server_default=func.now())
    
    category=relationship("Category", back_populates="products")
    supplier=relationship("Supplier", back_populates="products")
    sale_items = relationship("SaleItem", back_populates="product")