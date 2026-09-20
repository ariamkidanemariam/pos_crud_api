from sqlalchemy import(
    String,
    Text,
    Boolean,
    Column,
    UUID
)
import uuid
from database import Base
from sqlalchemy.orm import relationship

class Category(Base):
    __tablename__="categories"
    
    category_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, autoincrement=False)
    name= Column(String(50), nullable=False)
    description= Column(Text, nullable=True)
    is_active=Column(Boolean,nullable=False, default= True)

    products = relationship("Product", back_populates="category")
    