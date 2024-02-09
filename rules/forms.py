# forms.py
from django import forms

class TeamForm(forms.Form):
    teams = forms.CharField(label='Enter Teams (comma-separated)')
