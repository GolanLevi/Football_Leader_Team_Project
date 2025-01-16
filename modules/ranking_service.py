def calculate_team_score(matches, team_name):
    if not matches:
        return 0

    recent_results = 0
    goal_difference = 0

    for match in matches:
        if team_name in [match.get('team1'), match.get('team2')]:
            if match.get('team1') == team_name:
                if match.get('team1_score') > match.get('team2_score'):
                    recent_results += 3  # ניצחון
                elif match.get('team1_score') == match.get('team2_score'):
                    recent_results += 1  # תיקו
                goal_difference += match.get('team1_score') - match.get('team2_score')
            elif match.get('team2') == team_name:
                if match.get('team2_score') > match.get('team1_score'):
                    recent_results += 3  # ניצחון
                elif match.get('team2_score') == match.get('team1_score'):
                    recent_results += 1  # תיקו
                goal_difference += match.get('team2_score') - match.get('team1_score')

    return recent_results + goal_difference