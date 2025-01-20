from pymongo import MongoClient
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

# Connect to MongoDB
MONGO_URI = os.getenv("MONGO_URI")
client = MongoClient(MONGO_URI)
db = client["football-cluster"]

def get_collection(collection_name):
    """
    Get a collection from the database.
    """
    return db[collection_name]

def sync_data_to_cloud_bulk(local_collection_name, cloud_collection_name):
    local_collection = db[local_collection_name]
    cloud_collection = db[cloud_collection_name]

    docs = list(local_collection.find())
    if docs:
        operations = [
            MongoClient.UpdateOne(
                {"_id": doc["_id"]},
                {"$set": doc},
                upsert=True
            )
            for doc in docs
        ]
        cloud_collection.bulk_write(operations)
    print(f"Data synced from {local_collection_name} to {cloud_collection_name}")
