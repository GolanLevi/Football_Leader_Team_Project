def calculate_team_score(matches, team_name):
    """
    Calculate total points for a team based on its matches.
    """
    if not matches:
        return 0

    total_points = 0
    home_goal_difference = 0
    away_goal_difference = 0

    for match in matches:
        # Ensure score keys and relevant team data are present
        if (
            'score' in match
            and 'fullTime' in match['score']
            and 'home' in match['score']['fullTime']
            and 'away' in match['score']['fullTime']
            and match['score']['fullTime']['home'] is not None
            and match['score']['fullTime']['away'] is not None
        ):
            home_team = match.get('homeTeam', {}).get('name')
            away_team = match.get('awayTeam', {}).get('name')
            home_score = match['score']['fullTime']['home']
            away_score = match['score']['fullTime']['away']

            if team_name == home_team:
                # Home team logic
                if home_score > away_score:
                    total_points += 3
                    home_goal_difference += home_score - away_score
                elif home_score == away_score:
                    total_points += 1
            elif team_name == away_team:
                # Away team logic
                if away_score > home_score:
                    total_points += 6
                    away_goal_difference += (away_score - home_score) * 1.5
                elif away_score == home_score:
                    total_points += 2

    total_points += home_goal_difference + away_goal_difference
    return total_points
