from flask_restful import Resource, reqparse
from flask import jsonify
from database import db

class Teams(Resource):
    def get(self):
        """
        Get all teams
        ---
        tags:
          - Teams
        responses:
          200:
            description: List of all teams
        """
        teams = list(db.teams.find({}, {"_id": 0}))
        return jsonify(teams)

    def post(self):
        """
        Add a new team
        ---
        tags:
          - Teams
        parameters:
          - name: body
            in: body
            required: true
            schema:
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
        responses:
          201:
            description: Team added successfully
        """
        parser = reqparse.RequestParser()
        parser.add_argument('name', required=True)
        parser.add_argument('country', required=True)
        parser.add_argument('founded', type=int, required=True)
        parser.add_argument('stadium', required=True)
        args = parser.parse_args()
        db.teams.insert_one(args)
        return {"message": "Team added successfully"}, 201