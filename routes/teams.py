from flask import Blueprint, jsonify
from database import get_collection
from modules.ranking_service import calculate_team_score

teams_bp = Blueprint('teams', __name__)
rankings_bp = Blueprint('rankings', __name__)

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
                  crest:
                    type: string
                    description: URL of the team's crest.
                  venue:
                    type: string
                    description: Team's home stadium.
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
                  crest:
                    type: string
                    description: URL of the team's crest.
                  venue:
                    type: string
                    description: Team's home stadium.
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

        teams = list(collection.find({}))

        if teams:
            return jsonify({response_key: teams}), 200
        else:
            return jsonify({"error": f"No teams found for {response_key}"}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@rankings_bp.route('/team-rankings', methods=['GET'])
def get_team_rankings():
    """
    Get team rankings based on the custom scoring algorithm.
    ---
    tags:
      - Rankings
    summary: Get Team Rankings
    description: Get a list of all teams ranked by total points.
    responses:
      200:
        description: List of ranked teams with their details.
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
                    description: Team rank.
                  _id:
                    type: integer
                    description: Team ID.
                  name:
                    type: string
                    description: Team name.
                  crest:
                    type: string
                    description: URL of the team's crest.
                  total_points:
                    type: number
                    description: Total points calculated.
      500:
        description: Internal server error.
    """
    try:
        matches_pl_collection = get_collection("matches_pl")
        matches_pd_collection = get_collection("matches_pd")
        matches_cl_collection = get_collection("matches_cl")
        premier_league_teams_collection = get_collection("premier_league_teams")
        la_liga_teams_collection = get_collection("la_liga_teams")

        if (
            matches_pl_collection is None or
            matches_pd_collection is None or
            matches_cl_collection is None or
            premier_league_teams_collection is None or
            la_liga_teams_collection is None
        ):
            return jsonify({"error": "One or more collections not found"}), 404

        matches_pl = list(matches_pl_collection.find({}))
        matches_pd = list(matches_pd_collection.find({}))
        matches_cl = list(matches_cl_collection.find({}))
        all_matches = matches_pl + matches_pd + matches_cl

        all_teams = list(premier_league_teams_collection.find({}, {"_id": 1, "name": 1, "crest": 1})) + \
                    list(la_liga_teams_collection.find({}, {"_id": 1, "name": 1, "crest": 1}))

        rankings = []
        for team in all_teams:
            team_name = team.get("name")
            if not team_name:
                continue

            total_points = calculate_team_score(all_matches, team_name)
            rankings.append({
                "_id": team["_id"],
                "name": team_name,
                "crest": team.get("crest"),
                "total_points": total_points
            })

        rankings = sorted(rankings, key=lambda x: x["total_points"], reverse=True)
        for idx, team in enumerate(rankings, start=1):
            team["rank"] = idx

        return jsonify({"rankings": rankings}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500
