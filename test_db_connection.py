import os
from motor.motor_asyncio import AsyncIOMotorClient
import asyncio

async def test_connection():
    mongo_url = os.getenv('MONGO_URL', 'mongodb://localhost:27017')
    client = AsyncIOMotorClient(mongo_url)
    try:
        await client.admin.command("ping")
        print("Database is connected")

        databases = await client.list_database_names()
        if 'bookshelf' in databases:
            print("The 'bookshelf' database is available.")

            db = client['bookshelf']
            collections = await db.list_collection_names()
            if 'reviews' in collections:
                print("The 'books' collection is available.")
            else:
                print("The 'books' collection is NOT available.")
        else:
            print("The 'bookshelf' database is NOT available.")
    except Exception as e:
        print(f"Database connection failed: {e}")
    finally:
        client.close()

asyncio.run(test_connection())