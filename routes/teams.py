from flask_restful import Resource
from flask import jsonify
from database import db
from modules.ranking_service import calculate_team_score

class Teams(Resource):
    def get(self):
        """
        Get all teams with rankings
        ---
        tags:
          - Teams
        responses:
          200:
            description: List of all teams with rankings
        """
        try:
            teams = list(db.teams.find({}, {"_id": 0}))
            matches = list(db.matches.find({}, {"_id": 0}))

            for team in teams:
                team['score'] = calculate_team_score(matches, team['name'])

            teams = sorted(teams, key=lambda x: x['score'], reverse=True)
            return jsonify(teams)
        except Exception as e:
            return {"error": str(e)}, 500
