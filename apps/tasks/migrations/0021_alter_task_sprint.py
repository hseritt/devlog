# Generated by Django 3.2.17 on 2023-02-20 14:44

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('sprints', '0006_alter_sprint_description'),
        ('tasks', '0020_merge_0003_alter_task_sprint_0019_category_project'),
    ]

    operations = [
        migrations.AlterField(
            model_name='task',
            name='sprint',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='tasks', to='sprints.sprint'),
        ),
    ]
