# Generated by Django 3.2.16 on 2023-01-29 02:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sprints', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='sprint',
            name='name',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
    ]
