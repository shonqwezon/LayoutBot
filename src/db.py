import asyncio
import os

import motor.motor_asyncio

from src.utils import setup_logger

DB_URL = f"mongodb://{os.getenv('MONGO_INITDB_ROOT_USERNAME')}:{os.getenv('MONGO_INITDB_ROOT_PASSWORD')}@localhost:27017/"
db = motor.motor_asyncio.AsyncIOMotorClient(DB_URL)["app"]

logger = setup_logger(__name__)

