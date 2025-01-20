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

def sync_data_to_cloud(local_collection_name, cloud_collection_name):
    """
    Sync data from a local collection to a cloud collection.
    """
    local_collection = db[local_collection_name]
    cloud_collection = db[cloud_collection_name]

    # Iterate through all documents in the local collection and sync to cloud
    for doc in local_collection.find():
        cloud_collection.update_one({"_id": doc["_id"]}, {"$set": doc}, upsert=True)

    print(f"Data synced from {local_collection_name} to {cloud_collection_name}")

# Example: Call this function to sync collections
if __name__ == "__main__":
    sync_data_to_cloud("premier_league_teams", "premier_league_teams")
    sync_data_to_cloud("la_liga_teams", "la_liga_teams")
    sync_data_to_cloud("matches_pl", "matches_pl")
    sync_data_to_cloud("matches_pd", "matches_pd")
    sync_data_to_cloud("matches_cl", "matches_cl")
    sync_data_to_cloud("premier_league_players", "premier_league_players")
