# Generated by Django 3.2.17 on 2023-02-18 12:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sprints', '0001_squashed_0006_alter_sprint_status'),
    ]

    operations = [
        migrations.AlterField(
            model_name='sprint',
            name='status',
            field=models.CharField(choices=[('Open', 'Open'), ('Ended', 'Ended'), ('Future', 'Future')], default='Open', max_length=20),
        ),
    ]
