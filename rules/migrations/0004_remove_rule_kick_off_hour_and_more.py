# Generated by Django 4.1.1 on 2024-03-15 14:57

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('rules', '0003_rule_kick_off_hour_rule_kick_off_minute'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='rule',
            name='kick_off_hour',
        ),
        migrations.RemoveField(
            model_name='rule',
            name='kick_off_minute',
        ),
    ]
