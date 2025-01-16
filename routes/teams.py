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
        summary: Retrieve all teams sorted by their rankings
        description: This endpoint returns a list of all teams, including their ranking score, sorted in descending order.
        responses:
          200:
            description: A list of teams with rankings
            schema:
              type: array
              items:
                type: object
                properties:
                  name:
                    type: string
                    example: "Real Madrid"
                  country:
                    type: string
                    example: "Spain"
                  founded:
                    type: integer
                    example: 1902
                  stadium:
                    type: string
                    example: "Santiago Bernabeu"
                  score:
                    type: integer
                    example: 95
        """
        try:
            teams = list(db.teams.find({}, {"_id": 0}))
            matches = list(db.matches.find({}, {"_id": 0}))

            team_scores = []
            for team in teams:
                score = calculate_team_score(matches, team.get('name', 'Unknown'))
                team['score'] = score
                team_scores.append({
                    "name": team.get('name', 'Unknown'),
                    "country": team.get('area', {}).get('name', 'Unknown'),  # Using nested structure for country
                    "founded": team.get('founded', 'Unknown'),
                    "stadium": team.get('venue', 'Unknown'),  # Using venue for stadium
                    "score": score
                })

            team_scores = sorted(team_scores, key=lambda x: x['score'], reverse=True)

            return jsonify(team_scores)
        except Exception as e:
            return {"error": str(e)}, 500
