import json
import os

import motor.motor_asyncio
from bson import ObjectId

from src.utils import setup_logger

DB_URL = f"mongodb://{os.getenv('MONGO_INITDB_ROOT_USERNAME')}:{os.getenv('MONGO_INITDB_ROOT_PASSWORD')}@{os.getenv('MONGO_HOST')}:27017/"
COLLECTION_NAME = "dataset"
db = motor.motor_asyncio.AsyncIOMotorClient(DB_URL)[os.getenv("MONGO_DB_NAME")]

logger = setup_logger(__name__)


async def init_db(filepath: str, type: str, drop=False):
    if drop:
        await db[COLLECTION_NAME].drop()
    collection = db[COLLECTION_NAME]
    with open(filepath, "r", encoding="utf-8") as file:
        data = json.load(file)
    for body in data:
        query = {"body": body, "good": [], "bad": [], "type": type}
        await collection.insert_one(query)


async def export_data(info, type):
    if info[1] not in ["$gt", "$lt", "$eq"]:
        raise ValueError("Invalid operator. Use '$gt', '$lt', or '$eq'.")

    collection = db[COLLECTION_NAME]
    query = {"$expr": {info[1]: [{"$size": "$good"}, {"$size": "$bad"}]}, "type": type}
    documents = []
    async for document in collection.find(query):
        documents.append(document.get("body"))

    with open(type + "_" + info[0], "w", encoding="utf-8") as file:
        json.dump(documents, file, ensure_ascii=False, indent=4)


async def get_response(user_id: int):
    collection = db[COLLECTION_NAME]

    pipeline = [
        {
            "$match": {
                "$expr": {
                    "$lt": [
                        {"$add": [{"$size": "$good"}, {"$size": "$bad"}]},
                        3,
                    ]  # Sum of sizes < 3
                },
                "good": {"$nin": [user_id]},  # user_id not in 'good' array
                "bad": {"$nin": [user_id]},  # user_id not in 'bad' array
            }
        },
        {
            "$sample": {"size": 1}  # Randomly select 1 document
        },
    ]

    result = await collection.aggregate(pipeline).to_list(length=1)

    if result:
        return result[0]
    else:
        return None


async def update_response(doc_id: str, user_id: int, type: str):
    collection = db[COLLECTION_NAME]

    try:
        res = await collection.update_one(
            {"_id": ObjectId(doc_id)},
            {"$addToSet": {type: user_id}},
        )
        if res.modified_count != 1:
            logger.warning(
                f"Modified count = {res.modified_count}! Check out id = {doc_id}"
            )
    except Exception as e:
        logger.critical(f"Error updating document: {e}")


async def get_total_docs_len():
    collection = db[COLLECTION_NAME]
    try:
        total_count = await collection.count_documents({})
        return total_count
    except Exception as e:
        logger.critical(f"Error counting documents: {e}")
        return None


async def get_handled_docs_len():
    collection = db[COLLECTION_NAME]
    try:
        count = await collection.count_documents(
            {"$expr": {"$gte": [{"$add": [{"$size": "$good"}, {"$size": "$bad"}]}, 3]}}
        )
        return count
    except Exception as e:
        logger.critical(f"Error counting documents: {e}")
        return None
