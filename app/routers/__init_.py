from .category import router as category_router
from .customer import router as customer_router
from .payment import router as payment_router
from .receipt import router as receipt_router
from .sale_item import router as sale_item_router
from .sale import router as sale_router
from .supplier import router as supplier_router
from .user import router as user_router

__all__ = [
    "category_router",
    "customer_router",
    "payment_router",
    "receipt_router",
    "sale_item_router",
    "sale_router",
    "supplier_router",
    "user_router"
]
