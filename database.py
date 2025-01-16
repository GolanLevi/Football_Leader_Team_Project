import os
from dotenv import load_dotenv
from pymongo import MongoClient

load_dotenv()

db_password = os.getenv("DB_PASSWORD")
client = MongoClient(f"mongodb+srv://golanlevi121:{db_password}@football-cluster.fzjiw.mongodb.net/?retryWrites=true&w=majority")
db = client.football
