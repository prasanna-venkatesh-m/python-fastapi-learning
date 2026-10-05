from pymongo import AsyncMongoClient
from dotenv import load_dotenv
import os

load_dotenv()

mongo_uri = os.getenv("MONGO_DB_URI")
database_name = os.getenv("MONGO_DB_DATABASE_NAME")

client = AsyncMongoClient(mongo_uri)

database = client[database_name]

users_collection = database["users"]
