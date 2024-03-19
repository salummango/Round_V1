# In your app's urls.py
from django.urls import path
from . import views

urlpatterns = [
    # Other URL patterns
    path('', views.FixtureList, name='fixtures'),
    path('team_matches/', views.TeamMatches, name='team_matches'),
    path('TeamManager',views.team_manager_dashboard, name='team_manager_dashboard'),
]
