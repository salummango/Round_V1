# fixture.py
import itertools
from datetime import datetime, timedelta
from collections import defaultdict
from rules.models import Rule, Team
import random


def load_rules_from_database():
    """Load rules from the database."""
    rules = Rule.objects.all()
    return {rule.name: rule.value for rule in rules}


def generate_kickoff_times(kick_off_hour_values, kick_off_minute_values):
    """Generate all possible kick-off times based on the provided hour and minute values."""
    kickoff_times = set()
    for hour, minute in itertools.product(kick_off_hour_values, kick_off_minute_values):
        kickoff_times.add(f"{hour:02}:{minute:02}")
    return kickoff_times

def generate_double_round_robin_fixtures(teams, rules):
    """Generates a double round robin schedule with dates based on the given teams and rules."""
    num_teams = len(teams)
    num_rounds = 2 * (num_teams - 1)
    matches = []
    
    start_date_str = rules['LeagueStartDate']
    start_date = datetime.strptime(start_date_str, '%Y-%m-%d')
    
    weekend_rule = rules['WeekendScheduling']
    total_match_days_per_week = sum(weekend_rule.values())
    
    rotation_index = 0
    
    # Group teams by stadium and city
    stadiums = defaultdict(list)
    cities = defaultdict(list)
    for team in teams:
        stadiums[team.stadium].append(team)
        cities[team.city].append(team)
    
    # Extract kick-off hour and minute from the rules
    kick_off_hour_values = rules['kick_off_hour']
    kick_off_minute_values = rules['kick_off_minute']
    print("Kick-off hour values that are in database:", kick_off_hour_values)
    print("Kick-off minute values that are in database:", kick_off_minute_values)
    
    kickoff_times = generate_kickoff_times(kick_off_hour_values, kick_off_minute_values)

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
            
            # Randomly select a kick-off time from the set of all possible kick-off times
            kick_off_time = random.choice(list(kickoff_times))
            kickoff_times.remove(kick_off_time)  # Remove the selected time to avoid duplicate assignments

            print("Selected kick-off time:", kick_off_time)

            # Combine date and time to create MatchDateTime
            match_datetime = datetime.combine(match_date, datetime.strptime(kick_off_time, "%H:%M").time())

            round_matches.append((home_team, away_team, match_datetime))
            current_week_match_days -= 1
        
        teams = teams[1:] + teams[:1]
        matches.append(round_matches)
    
    return matches, start_date
