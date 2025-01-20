from pymongo import MongoClient, UpdateOne
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
    """
    Sync data from a local collection to a cloud collection.
    """
    try:
        local_collection = db[local_collection_name]
        cloud_collection = db[cloud_collection_name]

        docs = list(local_collection.find())
        if not docs:
            print(f"No documents found in {local_collection_name} to sync.")
            return

        # Prepare bulk operations
        operations = [
            UpdateOne(
                {"_id": doc["_id"]},  # Match by the document ID
                {"$set": doc},  # Update the document
                upsert=True  # Insert if it doesn't exist
            )
            for doc in docs
        ]

        # Execute bulk write
        result = cloud_collection.bulk_write(operations)
        print(f"Data synced from {local_collection_name} to {cloud_collection_name}:")
        print(f"Matched: {result.matched_count}, Inserted: {result.upserted_count}, Modified: {result.modified_count}")

    except Exception as e:
        print(f"Error syncing data from {local_collection_name} to {cloud_collection_name}: {e}")

if __name__ == "__main__":
    # Sync all relevant collections
    collections_to_sync = [
        ("premier_league_teams", "premier_league_teams"),
        ("la_liga_teams", "la_liga_teams"),
        ("matches_pl", "matches_pl"),
        ("matches_pd", "matches_pd"),
        ("matches_cl", "matches_cl"),
        ("premier_league_players", "premier_league_players")
    ]

    for local_collection, cloud_collection in collections_to_sync:
        sync_data_to_cloud_bulk(local_collection, cloud_collection)
