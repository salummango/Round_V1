# Generated by Django 4.1.1 on 2024-03-02 05:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('rules', '0004_fixture'),
    ]

    operations = [
        migrations.AddField(
            model_name='fixture',
            name='round_number',
            field=models.IntegerField(default=1),
        ),
    ]
