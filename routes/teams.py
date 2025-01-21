from flask import Blueprint, jsonify
from database import get_collection
from modules.ranking_service import calculate_team_score

teams_bp = Blueprint('teams', __name__)

@teams_bp.route('/premier-league', methods=['GET'])
def get_premier_league_teams():
    """
    Get all teams from the Premier League.
    ---
    tags:
      - Teams
    summary: Get Premier League Teams
    description: Get a list of all teams from the Premier League with full details.
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
        if collection is None:
            return jsonify({"error": "Collection not found"}), 404

        teams = list(collection.find({}, {"_id": 0}))
        if teams:
            return jsonify({"premier_league_teams": teams}), 200
        else:
            return jsonify({"error": "No teams found for Premier League"}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@teams_bp.route('/la-liga', methods=['GET'])
def get_la_liga_teams():
    """
    Get all teams from La Liga.
    ---
    tags:
      - Teams
    summary: Get La Liga Teams
    description: Get a list of all teams from La Liga with full details.
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
        if collection is None:
            return jsonify({"error": "Collection not found"}), 404

        teams = list(collection.find({}, {"_id": 0}))
        if teams:
            return jsonify({"la_liga_teams": teams}), 200
        else:
            return jsonify({"error": "No teams found for La Liga"}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@teams_bp.route('/premier-league-players', methods=['GET'])
def get_premier_league_players():
    """
    Get all players from the Premier League.
    ---
    tags:
      - Teams
    summary: Get Premier League Players
    description: Get a list of all players from the Premier League.
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
        if collection is None:
            return jsonify({"error": "Collection not found"}), 404

        players = list(collection.find({}, {"_id": 0}))
        if players:
            return jsonify({"premier_league_players": players}), 200
        else:
            return jsonify({"error": "No players found for Premier League"}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@teams_bp.route('/rankings', methods=['GET'])
def get_team_rankings():
    """
    Get rankings of the best teams based on the algorithm.
    ---
    tags:
      - Teams
    summary: Get Team Rankings
    description: Get rankings of the best teams using the custom ranking algorithm.
    responses:
      200:
        description: List of team rankings.
        schema:
          type: object
          properties:
            rankings:
              type: array
              items:
                type: object
                properties:
                  rank:
                    type: integer
                    example: 1
                  team_name:
                    type: string
                    example: "Manchester City"
                  total_points:
                    type: integer
                    example: 87
      500:
        description: Internal server error.
    """
    try:
        teams_collection = get_collection("premier_league_teams")
        matches_collection = get_collection("matches_pl")

        if teams_collection is None or matches_collection is None:
            return jsonify({"error": "One or more collections not found"}), 404

        teams = list(teams_collection.find({}, {"_id": 0}))
        matches = list(matches_collection.find({}, {"_id": 0}))

        rankings = []
        for team in teams:
            team_name = team.get("name")
            if team_name:
                total_points = calculate_team_score(matches, team_name)
                rankings.append({"team_name": team_name, "total_points": total_points})

        rankings = sorted(rankings, key=lambda x: x["total_points"], reverse=True)

        for index, team in enumerate(rankings, start=1):
            team["rank"] = index

        return jsonify({"rankings": rankings}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500
