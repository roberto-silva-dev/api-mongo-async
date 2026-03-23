from fastapi import APIRouter, HTTPException, BackgroundTasks
from fastapi.responses import JSONResponse
from app.events import publish_event
from beanie import PydanticObjectId
from app.models.order import Order, OrderItem
from datetime import datetime

router = APIRouter(prefix="/orders", tags=["orders"])

@router.get("")
async def get_orders():
    orders = await Order.find_all().to_list()
    return orders

@router.get("/{order_id}")
async def get_order(order_id: PydanticObjectId):
    order = await Order.get(order_id)
    if not order:
        raise HTTPException(status_code=404, detail="Pedido não encontrado")
    return order

@router.post(
    "",
    status_code=201,
    summary="Create a order",
    description="Create a order and put it to process"
)
async def create_order(order: Order, background_tasks: BackgroundTasks):
    order.status = "pending"
    order.created_at = datetime.utcnow()
    await order.insert()

    event = {
        "event": "order_created",
        "order_id": str(order.id)
    }
    background_tasks.add_task(publish_event, event)

    return {"id": str(order.id), "status": order.status}

@router.patch("/{order_id}/status")
async def update_status(order_id: PydanticObjectId, status: str):
    order = await Order.get(order_id)
    if not order:
        raise HTTPException(status_code=404, detail="Pedido não encontrado")

    await order.set({Order.status: status})
    return {"id": str(order.id), "status": order.status}

@router.delete("/{order_id}")
async def delete_order(order_id: PydanticObjectId):
    order = await Order.get(order_id)
    if not order:
        raise HTTPException(status_code=404, detail="Pedido não encontrado")

    await order.delete()
    return {"message": "Pedido deletado"}