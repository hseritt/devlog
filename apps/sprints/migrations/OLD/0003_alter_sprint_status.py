# Generated by Django 3.2.16 on 2023-01-29 02:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sprints', '0002_sprint_name'),
    ]

    operations = [
        migrations.AlterField(
            model_name='sprint',
            name='status',
            field=models.CharField(choices=[('Open', 'Open'), ('Ended', 'Ended')], default='Open', max_length=20),
        ),
    ]
