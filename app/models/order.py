from beanie import Document
from pydantic import BaseModel, ConfigDict
from datetime import datetime, timezone
from pydantic import Field
from enum import Enum


class OrderStatus(str, Enum):
    PENDING = "pending"
    PROCESSED = "processed"
    FAILED = "failed"
    CANCELLED = "cancelled"


class OrderItem(BaseModel):
    product_id: str
    quantity: int

class Order(Document):
    customer: str
    items: list[OrderItem]
    status: OrderStatus = OrderStatus.PENDING
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

    class Settings:
        name = "orders"
    
    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "customer": "Roberto Silva",
                "items": [
                    {"product_id": "prod_123", "quantity": 2}
                ]
            }
        }
    )