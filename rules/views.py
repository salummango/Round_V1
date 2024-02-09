# # views.py
# from django.shortcuts import redirect,render
# from .models import Rule, Team, Fixture
# from .fixture import generate_double_round_robin_fixtures

# def generate_fixtures_admin(request):
#     if request.method == 'POST':
#         teams = Team.objects.all()
#         rules = {rule.name: rule.value for rule in Rule.objects.all()}
#         fixtures, start_date = generate_double_round_robin_fixtures(teams, rules)
#         fixtures_list = []

#         for round_matches in fixtures:
#             for match in round_matches:
#                 fixture = Fixture(home_team=match[0], away_team=match[1], match_date=match[2])
#                 fixture.save()
#                 fixtures_list.append(fixture)

#         return render(request, 'fixtures.html', {'fixtures_list': fixtures_list, 'start_date': start_date})
#     else:
#         return render(request, 'generate_fixtures_admin.html')
