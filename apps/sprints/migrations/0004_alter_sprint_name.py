# Generated by Django 3.2.17 on 2023-02-18 12:23

import apps.sprints.models
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("sprints", "0003_alter_sprint_name"),
    ]

    operations = [
        migrations.AlterField(
            model_name="sprint",
            name="name",
            field=models.CharField(
                default=apps.sprints.models.Sprint.default_sprint_name, max_length=50
            ),
        ),
    ]
