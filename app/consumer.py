from bson import ObjectId
from app.db import orders_collection
import time


def process_order(event: dict):
    print("Aguardando 5s para então processar o evento...")
    time.sleep(10)
    print("⚙️ Processando evento:", event)

    order_id = event["order_id"]

    order = orders_collection.find_one({
        "_id": ObjectId(order_id)
    })

    if not order:
        print("Pedido não encontrado")
        return

    # 💣 Idempotência (obrigatório)
    if order.get("status") == "processed":
        print("Já processado, ignorando")
        return

    # Simula processamento
    print("Processando pagamento...")

    orders_collection.update_one(
        {"_id": ObjectId(order_id)},
        {"$set": {"status": "processed"}}
    )

    print("✅ Pedido processado")