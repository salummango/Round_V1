# Generated by Django 4.1.1 on 2024-03-15 15:05

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('rules', '0004_remove_rule_kick_off_hour_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='fixture',
            old_name='kickoff',
            new_name='KickoffTime',
        ),
    ]