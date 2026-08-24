import os
from dotenv import load_dotenv
from motor.motor_asyncio import AsyncIOMotorClient

load_dotenv()

Mongodb_url = os.getenv("DATABASE_URL")
database_name = os.getenv("DATABASE_NAME")

class Database:
    databse = None
    client = None


db = Database()


async def connect_database():
    print(f"Connecting to database")
    db.client = AsyncIOMotorClient(Mongodb_url)
    db.database = db.client[database_name]

    await db.client.admin.command("ping")

    print(f"connected to database")
   

def get_db_connection():
    return db.database


def close_db_connection():
    db.client.close()
    print("Mongodb connection closed")



