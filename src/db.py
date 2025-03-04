import json
import os

import motor.motor_asyncio

from src.utils import setup_logger

DB_URL = f"mongodb://{os.getenv('MONGO_INITDB_ROOT_USERNAME')}:{os.getenv('MONGO_INITDB_ROOT_PASSWORD')}@localhost:27017/"
COLLECTION_NAME = "dataset"
db = motor.motor_asyncio.AsyncIOMotorClient(DB_URL)[os.getenv("MONGO_DB_NAME")]

logger = setup_logger(__name__)


async def init_db(filepath: str, drop=False):
    if drop:
        await db[COLLECTION_NAME].drop()
    collection = db[COLLECTION_NAME]
    with open(filepath, "r", encoding="utf-8") as file:
        data = json.load(file)
    for body in data:
        query = {"body": body, "good": [], "bad": []}
        await collection.insert_one(query)


async def export_data(info):
    if info[1] not in ["$gt", "$lt", "$eq"]:
        raise ValueError("Invalid operator. Use '$gt', '$lt', or '$eq'.")

    collection = db[COLLECTION_NAME]
    query = {"$expr": {info[1]: [{"$size": "$good"}, {"$size": "$bad"}]}}
    documents = []
    async for document in collection.find(query):
        documents.append(document.get("body"))

    with open(info[0], "w", encoding="utf-8") as file:
        json.dump(documents, file, ensure_ascii=False, indent=4)
