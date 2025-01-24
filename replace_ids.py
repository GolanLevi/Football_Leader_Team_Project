# from pymongo import MongoClient
# from dotenv import load_dotenv
# import os
# import requests
#
# # Load environment variables
# load_dotenv()
#
# # Constants
# API_KEY = os.getenv("FOOTBALL_API_KEY")
# BASE_URL = "https://api.football-data.org/v4/"
# HEADERS = {"X-Auth-Token": API_KEY}
# MONGO_URI = os.getenv("MONGO_URI", "mongodb://localhost:27017/")
#
# # Connect to MongoDB
# client = MongoClient(MONGO_URI)
# db = client["football-cluster"]
#
# def fetch_and_insert_teams(competition, collection_name):
#     """
#     Fetch teams for a specific competition and insert relevant data into MongoDB.
#     """
#     url = f"{BASE_URL}competitions/{competition}/teams"
#     response = requests.get(url, headers=HEADERS)
#     response.raise_for_status()
#     teams = response.json().get("teams", [])
#
#     collection = db[collection_name]
#     collection.delete_many({})  # Clear existing data
#
#     for team in teams:
#         team_data = {
#             "_id": team.get("id"),
#             "name": team.get("name"),
#             "shortName": team.get("shortName"),
#             "tla": team.get("tla"),
#             "crest": team.get("crest"),
#             "address": team.get("address"),
#             "website": team.get("website"),
#             "founded": team.get("founded"),
#             "venue": team.get("venue"),
#             "runningCompetitions": team.get("runningCompetitions"),
#             "coach": team.get("coach"),
#             "squad": team.get("squad"),
#         }
#         collection.insert_one(team_data)
#     print(f"Inserted {len(teams)} teams into {collection_name}.")
#
# def fetch_and_insert_matches(competition, collection_name, start_year, end_year):
#     """
#     Fetch matches for a specific competition within a year range and insert relevant data into MongoDB.
#     """
#     url = f"{BASE_URL}competitions/{competition}/matches"
#     response = requests.get(url, headers=HEADERS)
#     response.raise_for_status()
#     matches = response.json().get("matches", [])
#
#     collection = db[collection_name]
#     collection.delete_many({})  # Clear existing data
#
#     count = 0
#     for match in matches:
#         season_start = int(match.get("season", {}).get("startDate", "0000")[:4])
#         if start_year <= season_start <= end_year:
#             match_data = {
#                 "_id": match.get("id"),
#                 "competition": match.get("competition"),
#                 "season": match.get("season"),
#                 "homeTeam": match.get("homeTeam"),
#                 "awayTeam": match.get("awayTeam"),
#                 "score": match.get("score"),
#             }
#             collection.insert_one(match_data)
#             count += 1
#     print(f"Inserted {count} matches into {collection_name}.")
#
# def main():
#     """
#     Fetch data from API and insert relevant data into MongoDB collections.
#     """
#     competitions = {
#         "PL": {"teams": "premier_league_teams", "matches": "matches_pl"},
#         "PD": {"teams": "la_liga_teams", "matches": "matches_pd"},
#         "CL": {"matches": "matches_cl"},
#     }
#
#     start_year = 2022
#     end_year = 2025
#
#     for competition, collections in competitions.items():
#         if "teams" in collections:
#             fetch_and_insert_teams(competition, collections["teams"])
#         if "matches" in collections:
#             fetch_and_insert_matches(competition, collections["matches"], start_year, end_year)
#
# if __name__ == "__main__":
#     main()
