import json
from app.redis_client import redis_client
from app.sqs_client import sqs, QUEUE_URL

# in memory
# queue = []
# def publish_event(event: dict):
#     print("📤 Publicando evento:", event)
#     queue.append(event)


# with redis
# QUEUE_NAME = "orders_queue"
# def publish_event(event: dict):
#     redis_client.lpush(QUEUE_NAME, json.dumps(event))
#     print("Evento publicado:", event)


# aws sqs
def publish_event(event: dict):
    event_name = event.get('event')
    print("Tentando publicar evento:", event_name)
    sqs.send_message(
        QueueUrl=QUEUE_URL,
        MessageBody=json.dumps(event)
    )
    print(f"Evento {event_name} publicado")