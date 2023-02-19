# Generated by Django 3.2.17 on 2023-02-19 00:16

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('tasks', '0001_squashed_0018_auto_20230214_2355'),
    ]

    operations = [
        migrations.AddField(
            model_name='task',
            name='last_action_by',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='task_last_action_by', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='task',
            name='assigned_to',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='task_assigned_to', to=settings.AUTH_USER_MODEL),
        ),
    ]
