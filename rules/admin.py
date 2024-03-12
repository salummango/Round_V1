# admin.py
from django.contrib import admin
from .models import Team, Fixture, Rule
from .fixture import generate_double_round_robin_fixtures
from import_export.admin import ImportExportModelAdmin
from import_export import resources

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
        for match in round_matches:
            home_team, away_team, match_date = match
            
            # Determine the stadium and city for the fixture
            match_stadium = home_team.stadium  # assign each team with it's stadium
            match_city = home_team.city  # assign each team with it's city
            
            fixture = Fixture(
                home_team=home_team,
                away_team=away_team,
                match_date=match_date,
                round_number=round_num,  
                match_stadium=match_stadium,
                match_city=match_city
            )
            fixture.save()


generate_fixtures.short_description = "Generate fixtures"

class TeamAdmin(admin.ModelAdmin):
    actions = [generate_fixtures]
    
    search_fields = ['name', 'city', 'stadium']
    list_display = ['name', 'city', 'stadium']
   

class FixtureResource(resources.ModelResource):#This class specifies the model to be used for importing and exporting data.
    class Meta:
        model = Fixture

class FixtureAdmin(ImportExportModelAdmin):
    resource_class = FixtureResource
    search_fields = ['home_team', 'away_team', 'match_date','match_stadium','match_city']
    list_display = ['round_number', 'id',  'home_team', 'away_team', 'match_date','match_stadium','match_city']
    ordering = ['round_number', 'id']

admin.site.register(Team, TeamAdmin)
admin.site.register(Fixture,FixtureAdmin)
admin.site.register(Rule)

