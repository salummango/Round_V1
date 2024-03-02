# your_script.py
import json
from datetime import datetime, timedelta
from rules.models import Rule, Team

def load_rules_from_database():
    """Load rules from the database."""
    rules = Rule.objects.all()
    return {rule.name: rule.value for rule in rules}

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

            round_matches.append((home_team, away_team, match_date.strftime('%Y-%m-%d')))
            current_week_match_days -= 1

        teams = teams[1:] + teams[:1]

        matches.append(round_matches)

    return matches, start_date
