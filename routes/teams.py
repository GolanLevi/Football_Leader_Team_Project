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

        teams = list(collection.find({}))

        for team in teams:
            team['_id'] = str(team['_id'])

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
def get_teams_rankings():
    """
    Get rankings of the best teams based on the algorithm.
    ---
    tags:
      - Teams
    summary: Get Teams Rankings
    description: Get rankings of the best teams using the custom ranking algorithm, including relevant Champions League matches.
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
                  team_name:
                    type: string
                  total_points:
                    type: integer
      500:
        description: Internal server error.
    """
    try:
        # Fetch collections
        matches_pl_collection = get_collection("matches_pl")
        matches_pd_collection = get_collection("matches_pd")
        matches_cl_collection = get_collection("matches_cl")
        premier_league_teams_collection = get_collection("premier_league_teams")
        la_liga_teams_collection = get_collection("la_liga_teams")

        # Check collections
        if (
            matches_pl_collection is None
            or matches_pd_collection is None
            or matches_cl_collection is None
            or premier_league_teams_collection is None
            or la_liga_teams_collection is None
        ):
            return jsonify({"error": "One or more collections not found"}), 404

        # Fetch matches
        matches_pl = list(matches_pl_collection.find({}, {"_id": 0}))
        matches_pd = list(matches_pd_collection.find({}, {"_id": 0}))

        # Fetch relevant Champions League matches
        premier_league_teams = list(premier_league_teams_collection.find({}, {"_id": 0, "name": 1}))
        la_liga_teams = list(la_liga_teams_collection.find({}, {"_id": 0, "name": 1}))
        all_relevant_teams = {team["name"] for team in premier_league_teams + la_liga_teams}

        matches_cl = list(
            matches_cl_collection.find(
                {
                    "$or": [
                        {"home_team": {"$in": list(all_relevant_teams)}},
                        {"away_team": {"$in": list(all_relevant_teams)}},
                    ]
                },
                {"_id": 0},
            )
        )

        # Combine matches
        all_matches = matches_pl + matches_pd + matches_cl

        # Process team rankings
        all_teams = premier_league_teams + la_liga_teams
        rankings = []
        for team in all_teams:
            team_name = team.get("name")
            if not team_name:
                continue

            # Calculate points for the team
            total_points = calculate_team_score(all_matches, team_name)
            rankings.append({"team_name": team_name, "total_points": total_points})

        # Sort rankings by total points
        rankings = sorted(rankings, key=lambda x: x["total_points"], reverse=True)

        # Add rank to each team
        for idx, rank in enumerate(rankings, start=1):
            rank["rank"] = idx

        return jsonify({"rankings": rankings}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500



