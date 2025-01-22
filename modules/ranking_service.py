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
        # Ensure score keys are present and not None
        if (
            'score' in match
            and 'home' in match['score']
            and 'away' in match['score']
            and match['score']['home'] is not None
            and match['score']['away'] is not None
        ):
            if team_name == match.get('home_team'):
                # Home team logic
                if match['score']['home'] > match['score']['away']:
                    total_points += 3
                    home_goal_difference += match['score']['home'] - match['score']['away']
                elif match['score']['home'] == match['score']['away']:
                    total_points += 1
                else:
                    total_points -= 3
            elif team_name == match.get('away_team'):
                # Away team logic
                if match['score']['away'] > match['score']['home']:
                    total_points += 6
                    away_goal_difference += (match['score']['away'] - match['score']['home']) * 1.5
                elif match['score']['away'] == match['score']['home']:
                    total_points += 2

    total_points += home_goal_difference + away_goal_difference
    return total_points
