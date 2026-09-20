from sqlalchemy import(
    String,
    Enum,
    DECIMAL,
    DateTime,
    Column, 
    ForeignKey,
    UUID
)
import enum
import uuid
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from database import Base

class PaymentMethod(str, enum.Enum):
    CASH = "cash"
    CREDIT_CARD = "credit_card"
    MOBILE_PAYMENT = "mobile_payment"
       
class PaymentStatus (str, enum.Enum):
    COMPLETED= "completed"
    FAILED="failed"
    REFUNDED= "refunded"
    
    
class Payment(Base):
    __tablename__="payments"
    
    
    payment_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, autoincrement=False)
    sale_id= Column(UUID(as_uuid=True), ForeignKey("sales.sale_id"), nullable=False)
    payment_method = Column(Enum(PaymentMethod, name="payment_method_enum"), nullable=True)
    amount= Column(DECIMAL(10,2), nullable= False)
    payment_date=Column(DateTime(timezone=True), server_default=func.now())
    status=Column(Enum(PaymentStatus, name="status_enum"), nullable=False)

    