import asyncio
from motor.motor_asyncio import AsyncIOMotorClient

async def test_mongo():
    mongo_url = "mongodb+srv://juniorpece_db_user:-g7bqQ%23Jb%25jAaR9@cluster0.q0jsudl.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"
    print("Testing connection...")
    try:
        client = AsyncIOMotorClient(mongo_url, serverSelectionTimeoutMS=5000)
        # Force a network request
        await client.admin.command('ping')
        print("Connected successfully!")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    asyncio.run(test_mongo())
