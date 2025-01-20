from flask import Flask, jsonify
from flasgger import Swagger
from flask_restful import Api
from database import db, get_collection

app = Flask(__name__)
swagger = Swagger(app)
api = Api(app)


@app.route('/db-check', methods=['GET'])
def db_check():
    """
    Check database connection and list collections.
    ---
    responses:
      200:
        description: Database is connected and collections are listed
        schema:
          type: object
          properties:
            message:
              type: string
              example: "Database is connected"
            collections:
              type: array
              items:
                type: string
      500:
        description: Internal server error
    """
    try:
        collections = db.list_collection_names()
        return jsonify({"message": "Database is connected", "collections": collections}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route('/premier-league-teams', methods=['GET'])
def get_premier_league_teams():
    """
    Get all teams from the Premier League with full details.
    ---
    responses:
      200:
        description: List of all Premier League teams with full details.
        schema:
          type: object
          properties:
            premier_league_teams:
              type: array
              items:
                type: object
      404:
        description: No teams found for Premier League.
      500:
        description: Internal server error.
    """
    try:
        collection = get_collection("premier_league_teams")
        if not collection:
            return jsonify({"error": "Collection not found"}), 404

        teams = list(collection.find({}, {"_id": 0}))
        if teams:
            return jsonify({"premier_league_teams": teams}), 200
        else:
            return jsonify({"error": "No teams found for Premier League"}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route('/la-liga-teams', methods=['GET'])
def get_la_liga_teams():
    """
    Get all teams from La Liga with full details.
    ---
    responses:
      200:
        description: List of all La Liga teams with full details.
        schema:
          type: object
          properties:
            la_liga_teams:
              type: array
              items:
                type: object
      404:
        description: No teams found for La Liga.
      500:
        description: Internal server error.
    """
    try:
        collection = get_collection("la_liga_teams")
        if not collection:
            return jsonify({"error": "Collection not found"}), 404

        teams = list(collection.find({}, {"_id": 0}))
        if teams:
            return jsonify({"la_liga_teams": teams}), 200
        else:
            return jsonify({"error": "No teams found for La Liga"}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route('/matches-pl', methods=['GET'])
def get_premier_league_matches():
    """
    Get all matches from the Premier League.
    ---
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
        if not collection:
            return jsonify({"error": "Collection not found"}), 404

        matches = list(collection.find({}, {"_id": 0}))
        if matches:
            return jsonify({"premier_league_matches": matches}), 200
        else:
            return jsonify({"error": "No matches found for Premier League"}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route('/matches-pd', methods=['GET'])
def get_la_liga_matches():
    """
    Get all matches from La Liga.
    ---
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
        if not collection:
            return jsonify({"error": "Collection not found"}), 404

        matches = list(collection.find({}, {"_id": 0}))
        if matches:
            return jsonify({"la_liga_matches": matches}), 200
        else:
            return jsonify({"error": "No matches found for La Liga"}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route('/matches-cl', methods=['GET'])
def get_champions_league_matches():
    """
    Get all matches from the Champions League.
    ---
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
        if not collection:
            return jsonify({"error": "Collection not found"}), 404

        matches = list(collection.find({}, {"_id": 0}))
        if matches:
            return jsonify({"champions_league_matches": matches}), 200
        else:
            return jsonify({"error": "No matches found for Champions League"}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route('/premier-league-players', methods=['GET'])
def get_premier_league_players():
    """
    Get all players from the Premier League.
    ---
    responses:
      200:
        description: List of all players from the Premier League.
        schema:
          type: object
          properties:
            premier_league_players:
              type: array
              items:
                type: object
      404:
        description: No players found for Premier League.
      500:
        description: Internal server error.
    """
    try:
        collection = get_collection("premier_league_players")
        if not collection:
            return jsonify({"error": "Collection not found"}), 404

        players = list(collection.find({}, {"_id": 0}))
        if players:
            return jsonify({"premier_league_players": players}), 200
        else:
            return jsonify({"error": "No players found for Premier League"}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
