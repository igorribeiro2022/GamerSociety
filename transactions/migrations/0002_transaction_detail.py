# Generated by Django 4.1.2 on 2022-11-08 17:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("transactions", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="transaction",
            name="detail",
            field=models.CharField(default="empty", max_length=250),
            preserve_default=False,
        ),
    ]
