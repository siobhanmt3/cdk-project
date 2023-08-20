import os
from motor.motor_asyncio import AsyncIOMotorClient


MONGO_INITDB_ROOT_USERNAME = os.getenv("MONGO_INITDB_ROOT_USERNAME")
MONGO_INITDB_ROOT_PASSWORD = os.getenv("MONGO_INITDB_ROOT_PASSWORD")

MONGODB_URI = os.getenv("MONGODB_URI")
async def get_db():
    mongodb_uri_local = f"mongodb://{MONGO_INITDB_ROOT_USERNAME}:{MONGO_INITDB_ROOT_PASSWORD}@db:27017"
    client = AsyncIOMotorClient(MONGODB_URI)
    return client.academia