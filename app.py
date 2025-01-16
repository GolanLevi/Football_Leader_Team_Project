from flask import Flask, jsonify
from flasgger import Swagger
from flask_restful import Api
from routes.teams import Teams
from routes.matches import Matches
from routes.statistics import Statistics
from modules.football_api import fetch_teams_from_api

app = Flask(__name__)
swagger = Swagger(app)
api = Api(app)

@app.route('/')
def home():
    return "Welcome to the Football API"

@app.route('/fetch-teams/<competition_id>', methods=['GET'])
def fetch_teams(competition_id):
    teams = fetch_teams_from_api(competition_id)
    if teams:
        for team in teams:
            db.teams.update_one(
                {"id": team["id"]},
                {"$set": team},
                upsert=True
            )
        return jsonify({"message": "Teams fetched and saved successfully"})
    else:
        return jsonify({"error": "Failed to fetch teams"}), 500

api.add_resource(Teams, '/teams')
api.add_resource(Matches, '/matches')
api.add_resource(Statistics, '/statistics')

if __name__ == '__main__':
    app.run(debug=True, host= "0.0.0.0", port=5000)
