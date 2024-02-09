# admin.py
from django.contrib import admin
from .models import Team, Fixture, Rule
from .fixture import generate_double_round_robin_fixtures

def generate_fixtures(modeladmin, request, queryset):
    teams = queryset.all()
    # Fetch rules from the database
    rules = {rule.name: rule.value for rule in Rule.objects.all()}
    fixtures, start_date = generate_double_round_robin_fixtures(teams, rules)

    for round_matches in fixtures:
        for match in round_matches:
            fixture = Fixture(home_team=match[0], away_team=match[1], match_date=match[2])
            fixture.save()

generate_fixtures.short_description = "Generate fixtures"

class TeamAdmin(admin.ModelAdmin):
    actions = [generate_fixtures]

admin.site.register(Team, TeamAdmin)
admin.site.register(Fixture)
admin.site.register(Rule)

