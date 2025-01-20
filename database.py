import os
from dotenv import load_dotenv
from pymongo import MongoClient

# Load environment variables
load_dotenv()

# MongoDB connection
db_password = os.getenv("DB_PASSWORD")
client = MongoClient(f"mongodb+srv://golanlevi121:{db_password}@football-cluster.fzjiw.mongodb.net/?retryWrites=true&w=majority")
db = client.football


def get_collection(collection_name):
    """
    Return a collection object based on its name.
    """
    try:
        return db[collection_name]
    except Exception as e:
        print(f"Error fetching collection {collection_name}: {e}")
        return None
