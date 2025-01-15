from flask_restful import Resource, reqparse
from flask import request, jsonify
from database import db

class Matches(Resource):
    def post(self):
        """
        Add a new match
        ---
        tags:
          - Matches
        parameters:
          - name: body
            in: body
            required: true
            schema:
              type: object
              properties:
                team1:
                  type: string
                  example: "Real Madrid"
                team2:
                  type: string
                  example: "Barcelona"
                team1_score:
                  type: integer
                  example: 2
                team2_score:
                  type: integer
                  example: 1
                date:
                  type: string
                  example: "2025-01-13"
        responses:
          201:
            description: Match added successfully
        """
        parser = reqparse.RequestParser()
        parser.add_argument('team1', required=True)
        parser.add_argument('team2', required=True)
        parser.add_argument('team1_score', type=int, required=True)
        parser.add_argument('team2_score', type=int, required=True)
        parser.add_argument('date', required=True)
        args = parser.parse_args()
        db.matches.insert_one(args)
        return {"message": "Match added successfully"}, 201
