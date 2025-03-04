import asyncio
from database import orders_collection, db

async def delete_orders():
    await orders_collection.delete_many({})  # Deletes all documents (orders)
    print("✅ All orders deleted.")

async def delete_database():
    await db.client.drop_database("orders_db")  # Drops entire database
    print("✅ Database 'orders_db' deleted.")

# Run deletion
if __name__ == "__main__":
    asyncio.run(delete_orders())  # or asyncio.run(delete_database())
