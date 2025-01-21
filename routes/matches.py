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
    description: Get a list of all matches from the Premier League.
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
      404:
        description: No matches found for Premier League.
      500:
        description: Internal server error.
    """
    try:
        collection = get_collection("matches_pl")
        if collection is None:
            return jsonify({"error": "Collection not found"}), 404

        matches = list(collection.find({}, {"_id": 0}))
        if matches:
            return jsonify({"premier_league_matches": matches}), 200
        else:
            return jsonify({"error": "No matches found for Premier League"}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@matches_bp.route('/pd', methods=['GET'])
def get_la_liga_matches():
    """
    Get all matches from La Liga.
    ---
    tags:
      - Matches
    summary: Get La Liga Matches
    description: Get a list of all matches from La Liga.
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
      404:
        description: No matches found for La Liga.
      500:
        description: Internal server error.
    """
    try:
        collection = get_collection("matches_pd")
        if collection is None:
            return jsonify({"error": "Collection not found"}), 404

        matches = list(collection.find({}, {"_id": 0}))
        if matches:
            return jsonify({"la_liga_matches": matches}), 200
        else:
            return jsonify({"error": "No matches found for La Liga"}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@matches_bp.route('/cl', methods=['GET'])
def get_champions_league_matches():
    """
    Get all matches from the Champions League.
    ---
    tags:
      - Matches
    summary: Get Champions League Matches
    description: Get a list of all matches from the Champions League.
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
      404:
        description: No matches found for Champions League.
      500:
        description: Internal server error.
    """
    try:
        collection = get_collection("matches_cl")
        if collection is None:
            return jsonify({"error": "Collection not found"}), 404

        matches = list(collection.find({}, {"_id": 0}))
        if matches:
            return jsonify({"champions_league_matches": matches}), 200
        else:
            return jsonify({"error": "No matches found for Champions League"}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 500
