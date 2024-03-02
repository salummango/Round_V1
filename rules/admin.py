# admin.py
from django.contrib import admin
from .models import Team, Fixture, Rule
from .fixture import generate_double_round_robin_fixtures

# def generate_fixtures(modeladmin, request, queryset):
#     teams = queryset.all()
#     # Fetch rules from the database
#     rules = {rule.name: rule.value for rule in Rule.objects.all()}
#     fixtures, start_date = generate_double_round_robin_fixtures(teams, rules)

    
#     for round_matches in fixtures:
#         for match in round_matches:
#             fixture = Fixture(home_team=match[0], away_team=match[1], match_date=match[2])
#             fixture.save()

# generate_fixtures.short_description = "Generate fixtures"


def generate_fixtures(modeladmin, request, queryset):
    teams = queryset.all()
    rules = {rule.name: rule.value for rule in Rule.objects.all()}
    fixtures, start_date = generate_double_round_robin_fixtures(teams, rules)

    for round_num, round_matches in enumerate(fixtures, start=1):
        # print(f"Round {round_num}:")
        for match in round_matches:
            home_team, away_team, match_date = match
            fixture = Fixture(
                home_team=home_team,
                away_team=away_team,
                match_date=match_date,
                round_number=round_num  # Assign round number to the fixture
            )
            fixture.save()
        #     print(f"{home_team} vs {away_team} - {match_date}")
        # print()

generate_fixtures.short_description = "Generate fixtures"

class TeamAdmin(admin.ModelAdmin):
    actions = [generate_fixtures]

class FixtureAdmin(admin.ModelAdmin):
    search_fields = ['home_team', 'away_team', 'match_date','id']

    list_display = ['id','round_number','home_team', 'away_team', 'match_date']
    ordering = ['round_number','id']

    


admin.site.register(Team, TeamAdmin)
admin.site.register(Fixture, FixtureAdmin)
admin.site.register(Rule)

