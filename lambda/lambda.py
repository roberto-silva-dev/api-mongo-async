import sys
import os
from datetime import datetime, timezone
from helpers import register_execution
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "libs"))
import json
from db import orders_collection
from bson import ObjectId
import traceback


def process_order(event: dict):
    start = datetime.now(timezone.utc)
    try:
        print("⚙️ Processando evento:", event)
        order_id = event["order_id"]
        if not ObjectId.is_valid(order_id):
            raise Exception(f"Invalid order_id type: {type(order_id)} [{order_id}]")
        
        order = orders_collection.find_one({
            "_id": ObjectId(order_id) 
        })

        if not order:
            raise Exception(f"Pedido {order_id} não encontrado")

        if order.get("status") == "processed":
            register_execution(order_id, "skipped", reason="already_processed", start=start, end=datetime.now(timezone.utc))
            print("Já processado, ignorando...")
            return

        print("Processando pagamento...")

        orders_collection.update_one(
            {"_id": ObjectId(order_id)},
            {"$set": {"status": "processed"}}
        )

        print("✅ Pedido processado")
        register_execution(order_id, "success", start=start, end=datetime.now(timezone.utc))
    except Exception as e:
        register_execution(
            order_id,
            "failed",
            error=e,
            traceback=traceback.format_exc(),
            start=start,
            end=datetime.now(timezone.utc)
        )
        raise



def handler(event, context):
    try:
        for record in event.get("Records", []):
            body = json.loads(record["body"])
            event_type = body.get("event")
            order_id = body.get("order_id")
            print(f"Processando: {event_type} - {order_id}")
            process_order(body)
    except Exception as e:
        print("Erro ao processar evento", e)
        raise

