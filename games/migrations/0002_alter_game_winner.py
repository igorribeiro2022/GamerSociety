# Generated by Django 4.1.2 on 2022-11-03 17:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("games", "0001_initial"),
    ]

    operations = [
        migrations.AlterField(
            model_name="game",
            name="winner",
            field=models.CharField(default=None, max_length=20, null=True),
        ),
    ]
