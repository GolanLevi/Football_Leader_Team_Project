def calculate_team_score(matches, team_name):
    if not matches:
        return 0

    total_points = 0
    home_goal_difference = 0
    away_goal_difference = 0

    for match in matches:
        if team_name == match.get('home_team'):
            if match['score']['fullTime']['home'] > match['score']['fullTime']['away']:
                total_points += 3
                home_goal_difference += match['score']['fullTime']['home'] - match['score']['fullTime']['away']
            elif match['score']['fullTime']['home'] == match['score']['fullTime']['away']:
                total_points += 1
            else:
                total_points -= 3
        elif team_name == match.get('away_team'):
            if match['score']['fullTime']['away'] > match['score']['fullTime']['home']:
                total_points += 6
                away_goal_difference += (match['score']['fullTime']['away'] - match['score']['fullTime']['home']) * 1.5
            elif match['score']['fullTime']['away'] == match['score']['fullTime']['home']:
                total_points += 2
            else:
                total_points += 0

    total_points += home_goal_difference + away_goal_difference
    return total_points
