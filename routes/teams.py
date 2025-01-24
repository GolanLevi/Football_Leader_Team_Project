from flask import Blueprint, jsonify
from database import get_collection

teams_bp = Blueprint('teams', __name__)

@teams_bp.route('/premier-league', methods=['GET'])
def get_premier_league_teams():
    """
    Get all teams from the Premier League.
    ---
    tags:
      - Teams
    summary: Get Premier League Teams
    description: Get a list of all Premier League teams with full details, including their IDs.
    responses:
      200:
        description: List of all teams from the Premier League.
        schema:
          type: object
          properties:
            premier_league_teams:
              type: array
              items:
                type: object
                properties:
                  _id:
                    type: integer
                    description: Team ID.
                  name:
                    type: string
                    description: Name of the team.
                  shortName:
                    type: string
                    description: Short name of the team.
                  tla:
                    type: string
                    description: Three-letter acronym of the team.
                  crest:
                    type: string
                    description: URL of the team's crest.
                  address:
                    type: string
                    description: Team's address.
                  website:
                    type: string
                    description: URL of the team's website.
                  founded:
                    type: integer
                    description: Year the team was founded.
                  venue:
                    type: string
                    description: Team's home stadium.
                  runningCompetitions:
                    type: array
                    items:
                      type: object
                      properties:
                        id:
                          type: integer
                        name:
                          type: string
                        code:
                          type: string
                        type:
                          type: string
                        emblem:
                          type: string
                  coach:
                    type: object
                    properties:
                      id:
                        type: integer
                      name:
                        type: string
                  squad:
                    type: array
                    items:
                      type: object
                      properties:
                        id:
                          type: integer
                        name:
                          type: string
                        position:
                          type: string
                        dateOfBirth:
                          type: string
                        nationality:
                          type: string
      404:
        description: No teams found for Premier League.
      500:
        description: Internal server error.
    """
    return fetch_teams("premier_league_teams", "premier_league_teams")


@teams_bp.route('/la-liga', methods=['GET'])
def get_la_liga_teams():
    """
    Get all teams from La Liga.
    ---
    tags:
      - Teams
    summary: Get La Liga Teams
    description: Get a list of all La Liga teams with full details, including their IDs.
    responses:
      200:
        description: List of all teams from La Liga.
        schema:
          type: object
          properties:
            la_liga_teams:
              type: array
              items:
                type: object
                properties:
                  _id:
                    type: integer
                    description: Team ID.
                  name:
                    type: string
                    description: Name of the team.
                  shortName:
                    type: string
                    description: Short name of the team.
                  tla:
                    type: string
                    description: Three-letter acronym of the team.
                  crest:
                    type: string
                    description: URL of the team's crest.
                  address:
                    type: string
                    description: Team's address.
                  website:
                    type: string
                    description: URL of the team's website.
                  founded:
                    type: integer
                    description: Year the team was founded.
                  venue:
                    type: string
                    description: Team's home stadium.
                  runningCompetitions:
                    type: array
                    items:
                      type: object
                      properties:
                        id:
                          type: integer
                        name:
                          type: string
                        code:
                          type: string
                        type:
                          type: string
                        emblem:
                          type: string
                  coach:
                    type: object
                    properties:
                      id:
                        type: integer
                      name:
                        type: string
                  squad:
                    type: array
                    items:
                      type: object
                      properties:
                        id:
                          type: integer
                        name:
                          type: string
                        position:
                          type: string
                        dateOfBirth:
                          type: string
                        nationality:
                          type: string
      404:
        description: No teams found for La Liga.
      500:
        description: Internal server error.
    """
    return fetch_teams("la_liga_teams", "la_liga_teams")


def fetch_teams(collection_name, response_key):
    """
    Helper function to fetch teams from a given collection.
    """
    try:
        collection = get_collection(collection_name)
        if collection is None:
            return jsonify({"error": f"Collection {collection_name} not found"}), 404

        # Include `_id` in the output
        teams = list(collection.find({}))

        if teams:
            return jsonify({response_key: teams}), 200
        else:
            return jsonify({"error": f"No teams found for {response_key}"}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 500
