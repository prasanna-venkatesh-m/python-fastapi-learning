from pymongo import AsyncMongoClient
from dotenv import load_dotenv
import os

load_dotenv()

mongo_uri = os.getenv("MONGO_DB_URI")
database_name = os.getenv("MONGO_DB_DATABASE_NAME")

if not mongo_uri:
    raise ValueError("MONGO_DB_URI is not configured")

if not database_name:
    raise ValueError("MONGO_DB_DATABASE_NAME is not configured")

client = AsyncMongoClient(
    mongo_uri,
    uuidRepresentation="standard"
)

database = client[database_name]

users_collection = database["users"]
