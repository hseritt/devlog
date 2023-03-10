# Generated by Django 3.2.16 on 2023-01-29 14:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tasks', '0005_task_blocked_by_tasks'),
    ]

    operations = [
        migrations.AlterField(
            model_name='task',
            name='type',
            field=models.CharField(choices=[('Feature', 'Feature'), ('Bug', 'Bug'), ('Task', 'Task'), ('Story', 'Story'), ('Epic', 'Epic'), ('Spike', 'Spike')], default='Task', max_length=30),
        ),
    ]
