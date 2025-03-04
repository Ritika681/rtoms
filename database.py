from motor.motor_asyncio import AsyncIOMotorClient
import os

# MongoDB Connection URL (Use environment variables or hardcode it)
MONGO_URL = os.getenv("MONGO_URL", "mongodb://localhost:27017")

# Create MongoDB client
client = AsyncIOMotorClient(MONGO_URL)
db = client.orders_db  # Database name
orders_collection = db.orders  # Collection name
