from flask_restful import Resource
from flask import jsonify
from database import db

class Statistics(Resource):
    def get(self):
        """
        Get match statistics
        ---
        tags:
          - Statistics
        responses:
          200:
            description: Match statistics
            content:
              application/json:
                schema:
                  type: object
                  properties:
                    totalMatches:
                      type: integer
        """
        try:
            matches = list(db.matches.find({}, {"_id": 0}))
            stats = {"totalMatches": len(matches)}
            return jsonify(stats)
        except Exception as e:
            return {"error": str(e)}, 500
