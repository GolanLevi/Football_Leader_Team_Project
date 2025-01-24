from flask import Blueprint, jsonify
from database import get_collection

matches_bp = Blueprint('matches', __name__)

@matches_bp.route('/pl', methods=['GET'])
def get_premier_league_matches():
    """
    Get all matches from the Premier League.
    ---
    tags:
      - Matches
    summary: Get Premier League Matches
    description: Get a list of all matches from the Premier League with detailed match information.
    responses:
      200:
        description: List of all matches from the Premier League.
        schema:
          type: object
          properties:
            premier_league_matches:
              type: array
              items:
                type: object
                properties:
                  _id:
                    type: integer
                    description: Match ID.
                  competition:
                    type: object
                    properties:
                      id:
                        type: integer
                      name:
                        type: string
                      code:
                        type: string
                      emblem:
                        type: string
                  season:
                    type: object
                    properties:
                      id:
                        type: integer
                      startDate:
                        type: string
                      endDate:
                        type: string
                      currentMatchday:
                        type: integer
                  homeTeam:
                    type: object
                    properties:
                      id:
                        type: integer
                      name:
                        type: string
                      shortName:
                        type: string
                      tla:
                        type: string
                      crest:
                        type: string
                  awayTeam:
                    type: object
                    properties:
                      id:
                        type: integer
                      name:
                        type: string
                      shortName:
                        type: string
                      tla:
                        type: string
                      crest:
                        type: string
                  score:
                    type: object
                    properties:
                      winner:
                        type: string
                      fullTime:
                        type: object
                        properties:
                          home:
                            type: integer
                          away:
                            type: integer
                      halfTime:
                        type: object
                        properties:
                          home:
                            type: integer
                          away:
                            type: integer
      404:
        description: No matches found for Premier League.
      500:
        description: Internal server error.
    """
    return fetch_matches("matches_pl", "premier_league_matches")


@matches_bp.route('/pd', methods=['GET'])
def get_la_liga_matches():
    """
    Get all matches from La Liga.
    ---
    tags:
      - Matches
    summary: Get La Liga Matches
    description: Get a list of all matches from La Liga with detailed match information.
    responses:
      200:
        description: List of all matches from La Liga.
        schema:
          type: object
          properties:
            la_liga_matches:
              type: array
              items:
                type: object
                properties:
                  _id:
                    type: integer
                    description: Match ID.
    """
    return fetch_matches("matches_pd", "la_liga_matches")


@matches_bp.route('/cl', methods=['GET'])
def get_champions_league_matches():
    """
    Get all matches from the Champions League.
    ---
    tags:
      - Matches
    summary: Get Champions League Matches
    description: Get a list of all matches from the Champions League with detailed match information.
    responses:
      200:
        description: List of all matches from the Champions League.
        schema:
          type: object
          properties:
            champions_league_matches:
              type: array
              items:
                type: object
                properties:
                  _id:
                    type: integer
                    description: Match ID.
    """
    return fetch_matches("matches_cl", "champions_league_matches")


def fetch_matches(collection_name, response_key):
    """
    Helper function to fetch matches from a given collection.
    """
    try:
        collection = get_collection(collection_name)
        if collection is None:
            return jsonify({"error": f"Collection {collection_name} not found"}), 404

        # Include `_id` in the output
        matches = list(collection.find({}))

        if matches:
            return jsonify({response_key: matches}), 200
        else:
            return jsonify({"error": f"No matches found for {response_key}"}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 500
