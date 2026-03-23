from pydantic_settings import BaseSettings
from pydantic import ConfigDict

class Settings(BaseSettings):
    # MongoDB
    mongo_url: str
    mongo_db: str = "orders_db"

    # AWS
    aws_region: str
    aws_access_key_id: str
    aws_secret_access_key: str
    queue_url: str

    model_config = ConfigDict(env_file=".env")

settings = Settings()