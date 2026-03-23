# only when using redis
from app.redis_client import redis_client
from app.consumer import process_order
import json

QUEUE_NAME = "orders_queue"


def consume():
    print("Consumer iniciado...")

    while True:
        _, raw = redis_client.brpop(QUEUE_NAME)  # bloqueia até ter item
        event = json.loads(raw)
        print("Evento identificado, processamento solicitado!")
        process_order(event)


if __name__ == "__main__":
    consume()