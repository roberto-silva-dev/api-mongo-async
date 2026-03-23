from pymongo import MongoClient
from helpers import get_parameter_from_aws_ssm

MONGO_URL = get_parameter_from_aws_ssm("mongodb-connection-string")

client = MongoClient(MONGO_URL)
db = client["orders_db"]

orders_collection = db["orders"]