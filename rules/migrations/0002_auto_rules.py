from django.db import migrations


def insert_initial_data(apps, schema_editor):
    Rule = apps.get_model('rules', 'Rule')
    initial_data = [
        {
            "name": "WeekendScheduling",
            "value": {
                "Friday": 1,
                "Saturday": 4,
                "Sunday": 3
            }
        },
        {
            "name": "LeagueStartDate",
            "value": "2024-01-05"
        },
        {
            "name":"kick_off_hour",
            "value": [16, 17, 18, 19]
        },
        {
            "name":"kick_off_minute",
            "value": [0, 15, 30, 45]
        }
    ]
    for data in initial_data:
        Rule.objects.create(name=data['name'], value=data['value'])



class Migration(migrations.Migration):

    dependencies = [
        ('rules', '0001_initial'),  # Add the appropriate previous migration number
    ]

    operations = [
        migrations.RunPython(insert_initial_data),
    ]
