from flask_restful import Resource, reqparse
from flask import jsonify
from database import db

class Matches(Resource):
    def get(self):
        """
        Get matches with optional filters (year, league)
        ---
        tags:
          - Matches
        summary: Retrieve matches with optional filters
        description: This endpoint retrieves matches and supports filtering by year and league.
        parameters:
          - name: year
            in: query
            required: false
            description: The year of the matches
            schema:
              type: integer
              example: 2022
          - name: league
            in: query
            required: false
            description: The league of the matches (e.g., "La Liga", "Premier League")
            schema:
              type: string
              example: "La Liga"
        responses:
          200:
            description: A list of matches
        """
        parser = reqparse.RequestParser()
        parser.add_argument('year', type=int, required=False, help="Year of the matches")
        parser.add_argument('league', type=str, required=False, help="League of the matches")
        args = parser.parse_args()

        filters = {}
        if args['year']:
            filters['date'] = {"$regex": f"^{args['year']}"}
        if args['league']:
            filters['league'] = args['league']

        try:
            matches = list(db.matches.find(filters, {"_id": 0}))
            return jsonify(matches)
        except Exception as e:
            return {"error": str(e)}, 500
