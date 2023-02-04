# Generated by Django 3.2.16 on 2023-02-04 13:43

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('projects', '0003_project_members'),
    ]

    operations = [
        migrations.AddField(
            model_name='project',
            name='manager',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='project_manager', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='project',
            name='members',
            field=models.ManyToManyField(blank=True, related_name='project_members', to=settings.AUTH_USER_MODEL),
        ),
    ]
