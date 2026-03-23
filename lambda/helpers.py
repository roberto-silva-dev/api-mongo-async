import boto3
from datetime import datetime, timezone


def get_parameter_from_aws_ssm(name):
    """
    Get a parameter from AWS SSM.
    Needs ssm:GetParameter permission to lambda/resource role
    """
    ssm = boto3.client("ssm")
    response = ssm.get_parameter(Name=name, WithDecryption=True)
    return response["Parameter"]["Value"]


dynamodb = boto3.resource("dynamodb")
table = dynamodb.Table("lambda_orders_consumer_execs")

def register_execution(order_id, status, error=None, duration_ms=None, start=None, end=None, reason=None, traceback=None):
    if not duration_ms and start and end:
        duration_ms = int((end - start).total_seconds() * 1000)

    item = {
        "order_id": order_id,
        "executed_at": datetime.now(timezone.utc).isoformat(),
        "status": status,  # "success" ou "failed"
    }

    if error:
        item["error"] = str(error)
    if duration_ms:
        item["duration_ms"] = duration_ms
    if reason:
        item["reason"] = reason  # "already_processed"
    if traceback:
        item["traceback"] = traceback
    table.put_item(Item=item)
