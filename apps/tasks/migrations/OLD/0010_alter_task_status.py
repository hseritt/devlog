# Generated by Django 3.2.16 on 2023-01-29 17:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tasks', '0009_alter_task_status'),
    ]

    operations = [
        migrations.AlterField(
            model_name='task',
            name='status',
            field=models.CharField(choices=[('New', 'New'), ('Investigation', 'Investigation'), ('In Progress', 'In Progress'), ('Awaiting Review', 'Awaiting Review'), ('In Review', 'In Review'), ('Awaiting Deployment', 'Awaiting Deployment'), ('Closed', 'Closed'), ("Won't Fix", "Won't Fix")], default='New', max_length=30),
        ),
    ]
