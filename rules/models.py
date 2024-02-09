# myapp/models.py
from django.db import models
import json

class Rule(models.Model):
    name = models.CharField(max_length=255, unique=True)
    value = models.JSONField()

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        # Ensure value is stored as JSON
        if isinstance(self.value, dict) or isinstance(self.value, list):
            self.value = json.dumps(self.value)
        super().save(*args, **kwargs)


class Team(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name
    
    
class Fixture(models.Model):
    home_team = models.CharField(max_length=100)
    away_team = models.CharField(max_length=100)
    match_date = models.DateField()

    def __str__(self):
        return f"{self.home_team} vs {self.away_team} - {self.match_date}"