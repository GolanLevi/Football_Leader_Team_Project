from database import db

teams = [
    {
        "name": "Real Madrid",
        "country": "Spain",
        "founded": 1902,
        "stadium": "Santiago Bernabeu"
    },
    {
        "name": "Barcelona",
        "country": "Spain",
        "founded": 1899,
        "stadium": "Camp Nou"
    }
]

matches = [
    {
        "team1": "Real Madrid",
        "team2": "Barcelona",
        "team1_score": 2,
        "team2_score": 1,
        "date": "2025-01-13"
    },
    {
        "team1": "Barcelona",
        "team2": "Real Madrid",
        "team1_score": 3,
        "team2_score": 2,
        "date": "2025-01-20"
    }
]

if db.teams.count_documents({}) == 0:
    db.teams.insert_many(teams)

if db.matches.count_documents({}) == 0:
    db.matches.insert_many(matches)
