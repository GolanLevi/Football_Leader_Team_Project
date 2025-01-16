import requests
import os
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("FOOTBALL_API_KEY")
BASE_URL = "https://api.football-data.org/v4/"
headers = {"X-Auth-Token": API_KEY}

def fetch_teams_from_api(competition_id):
    url = f"{BASE_URL}competitions/{competition_id}/teams"
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        return response.json().get("teams", [])
    else:
        return []
