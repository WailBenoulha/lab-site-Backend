# Generated by Django 5.2 on 2025-04-24 16:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("core", "0001_initial"),
    ]

    operations = [
        migrations.AlterField(
            model_name="message",
            name="reply",
            field=models.TextField(null=True),
        ),
    ]
