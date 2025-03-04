import asyncio
from database import orders_collection

sample_orders = [
    {"orderId": 1, "status": "Processing", "items": ["item1", "item2"], "tracking": "In warehouse"},
    {"orderId": 2, "status": "Shipped", "items": ["item3"], "tracking": "Out for delivery"},
    {"orderId": 3, "status": "Delivered", "items": ["item4", "item5"], "tracking": "Delivered"},
    {"orderId": 4, "status": "Shipped...", "items": ["item3"], "tracking": "Out for delivery"},
    {"orderId": 5, "status": "Delivered.....", "items": ["item4", "item5"], "tracking": "Delivered"}
]


async def insert_sample_orders():
    existing_order = await orders_collection.find_one({"orderId": 1})
    if not existing_order:
        await orders_collection.insert_many(sample_orders)
        print("✅ Sample orders inserted into MongoDB.")
    else:
        print("⚠️ Sample orders already exist. Skipping insert.")

# Run the function
if __name__ == "__main__":
    asyncio.run(insert_sample_orders())
