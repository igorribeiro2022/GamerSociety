# Generated by Django 4.1.2 on 2022-11-03 15:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("teams", "0001_initial"),
    ]

    operations = [
        migrations.AlterField(
            model_name="team",
            name="losses",
            field=models.PositiveIntegerField(default=0),
        ),
        migrations.AlterField(
            model_name="team",
            name="wins",
            field=models.PositiveIntegerField(default=0),
        ),
    ]
