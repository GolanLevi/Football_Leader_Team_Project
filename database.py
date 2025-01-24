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

def sync_data_to_cloud_bulk(local_collection_name, cloud_collection_name, identifier_field):
    """
    Sync data from a local collection to a cloud collection using a custom identifier field.
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
                {identifier_field: doc[identifier_field]},  # Match by the custom identifier
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
    # Sync all relevant collections with their custom identifiers
    collections_to_sync = [
        ("premier_league_teams", "premier_league_teams", "team_name"),  # Sync teams by team_name
        ("la_liga_teams", "la_liga_teams", "team_name"),  # Sync teams by team_name
        ("matches_pl", "matches_pl", "match_id"),  # Sync matches by match_id
        ("matches_pd", "matches_pd", "match_id"),  # Sync matches by match_id
        ("matches_cl", "matches_cl", "match_id"),  # Sync matches by match_id
        ("premier_league_players", "premier_league_players", "_id")  # Sync players by _id (no changes here)
    ]

    for local_collection, cloud_collection, identifier_field in collections_to_sync:
        sync_data_to_cloud_bulk(local_collection, cloud_collection, identifier_field)
