# Generated by Django 4.1.1 on 2024-01-27 07:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('rules', '0003_team'),
    ]

    operations = [
        migrations.CreateModel(
            name='Fixture',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('home_team', models.CharField(max_length=100)),
                ('away_team', models.CharField(max_length=100)),
                ('match_date', models.DateField()),
            ],
        ),
    ]