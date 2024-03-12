from datetime import datetime, timedelta
from collections import defaultdict
from rules.models import Rule, Team

def generate_double_round_robin_fixtures(teams, rules):
    """Generates a double round robin schedule with dates based on the given teams and rules."""
    
    # Extract necessary rules
    start_date_str = rules.get('LeagueStartDate')
    weekend_rule = rules.get('WeekendScheduling')
    home_away_balance_rule = rules.get('HomeAwayBalance')
    
    start_date = datetime.strptime(start_date_str, '%Y-%m-%d')
    
    num_teams = len(teams)
    num_rounds = 2 * (num_teams - 1)
    matches = []
    
    rotation_index = 0
    
    # Group teams by stadium and city
    stadiums = defaultdict(list)
    cities = defaultdict(list)
    for team in teams:
        stadiums[team.stadium].append(team)
        cities[team.city].append(team)
    
    # Track the match sequence for each team
    team_match_sequence = defaultdict(list)
    
    for i in range(num_rounds):
        round_matches = []
        
        half = num_teams // 2
        first_half = teams[:half]
        second_half = teams[half:]
        
        current_week_match_days = 0
        
        for j in range(half):
            if i % 2 == 0:
                home_team, away_team = first_half[j], second_half[-(j + 1)]
            else:
                home_team, away_team = second_half[-(j + 1)], first_half[j]
            
            while current_week_match_days == 0:
                match_date = start_date + timedelta(days=rotation_index)
                current_week_match_days = weekend_rule.get(match_date.strftime('%A'), 0)
                rotation_index += 1
            
            # Check StadiumSharing rule
            if home_team.stadium == away_team.stadium:
                rotation_index += 1
                match_date = start_date + timedelta(days=rotation_index)
            
            # Check SameCity rule
            if len(cities[home_team.city]) > 2:
                rotation_index += 1
                match_date = start_date + timedelta(days=rotation_index)
            
            round_matches.append((home_team, away_team, match_date.strftime('%Y-%m-%d')))
            current_week_match_days -= 1
            
            # Track the match sequence for each team
            team_match_sequence[home_team].append('H')
            team_match_sequence[away_team].append('A')
            
            # Check the HomeAwayBalance rule after each match assignment
            check_home_away_balance(home_team, team_match_sequence, home_away_balance_rule)
            check_home_away_balance(away_team, team_match_sequence, home_away_balance_rule)
        
        teams = teams[1:] + teams[:1]
        matches.append(round_matches)
    
    return matches, start_date

def check_home_away_balance(team, team_match_sequence, home_away_balance_rule):
    """Check the HomeAwayBalance rule for the given team."""
    sequence = team_match_sequence[team]
    if len(sequence) >= 5:
        consecutive_matches = sequence[-5:]
        home_count_rule = int(home_away_balance_rule[0])
        away_count_rule = int(home_away_balance_rule[2])
        home_count = consecutive_matches.count('H')
        away_count = consecutive_matches.count('A')
        
        if home_count != home_count_rule or away_count != away_count_rule:
            print(f"Warning: HomeAwayBalance not achievable for {team} in current schedule.")
