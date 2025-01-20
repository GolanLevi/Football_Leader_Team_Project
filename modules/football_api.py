import requests
import os
import logging
from pymongo import MongoClient
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Configuration Variables
API_KEY = os.getenv("FOOTBALL_API_KEY")
BASE_URL = "https://api.football-data.org/v4/"
HEADERS = {"X-Auth-Token": API_KEY}
MONGO_URI = os.getenv("MONGO_URI", "mongodb://localhost:27017/")

# Initialize Logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Database Connection
def connect_to_db():
    """Connect to MongoDB and return the database instance."""
    client = MongoClient(MONGO_URI)
    return client["football-cluster"]

def fetch_data_from_api(endpoint):
    """Generic function to fetch data from the Football API."""
    url = f"{BASE_URL}{endpoint}"
    try:
        response = requests.get(url, headers=HEADERS)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        logging.error(f"Error fetching data from {url}: {e}")
        return {}

def save_to_db(collection, query, data):
    """Generic function to save data to MongoDB."""
    try:
        collection.update_one(query, {"$set": data}, upsert=True)
    except Exception as e:
        logging.error(f"Error saving data to DB: {e}")

def fetch_teams(league_code, db):
    """Fetch and save teams for a given league."""
    endpoint = f"competitions/{league_code}/teams"
    data = fetch_data_from_api(endpoint)
    teams = data.get("teams", [])

    if teams:
        if league_code == "PL":
            collection = db["premier_league_teams"]
        elif league_code == "PD":
            collection = db["la_liga_teams"]
            for team in teams:
                save_to_db(collection, {"id": team["id"]}, team)
    return teams

def fetch_matches(league_code, season, db):
    """Fetch and save matches for a given league and season."""
    endpoint = f"competitions/{league_code}/matches?season={season}"
    data = fetch_data_from_api(endpoint)
    matches = data.get("matches", [])

    if matches:
        collection = db["matches"]
        for match in matches:
            query = {
                "home_team": match["homeTeam"].get("name"),
                "away_team": match["awayTeam"].get("name"),
                "date": match.get("utcDate"),
                "season": season
            }
            save_to_db(collection, query, match)
    return matches

def fetch_champions_league_matches(db):
    """Fetch and save Champions League matches."""
    endpoint = "competitions/CL/matches"
    data = fetch_data_from_api(endpoint)
    matches = data.get("matches", [])

    if matches:
        collection = db["champions_league_matches"]
        for match in matches:
            query = {
                "home_team": match["homeTeam"].get("name"),
                "away_team": match["awayTeam"].get("name"),
                "date": match.get("utcDate")
            }
            save_to_db(collection, query, match)
    return matches

def fetch_and_save_data():
    """Main function to fetch and save all relevant football data."""
    db = connect_to_db()

    # Fetch teams
    premier_league_teams = fetch_teams("PL", db)
    la_liga_teams = fetch_teams("PD", db)

    # Fetch matches
    seasons = [2025, 2024, 2023, 2022]
    for season in seasons:
        fetch_matches("PL", season, db)
        fetch_matches("PD", season, db)

    # Fetch Champions League matches
    fetch_champions_league_matches(db)

if __name__ == "__main__":
    fetch_and_save_data()
