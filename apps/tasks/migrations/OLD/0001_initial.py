# Generated by Django 3.2.16 on 2023-01-25 22:02

from django.conf import settings
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('projects', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Task',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('subject', models.CharField(max_length=100, unique=True)),
                ('description', models.TextField(blank=True, null=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('modified', models.DateTimeField(auto_now=True)),
                ('status', models.CharField(choices=[('New', 'New'), ('Investigation', 'Investigation'), ('In Progress', 'In Progress'), ('Awaiting Review', 'Awaiting Review'), ('In Review', 'In Review'), ('Awaiting Deployment', 'Awaiting Deployment'), ('Deployed', 'Deployed'), ('Closed', 'Closed')], default='New', max_length=30)),
                ('effort', models.IntegerField(default=5, validators=[django.core.validators.MaxValueValidator(10), django.core.validators.MinValueValidator(1)])),
                ('type', models.CharField(choices=[('Feature', 'Feature'), ('Bug', 'Bug'), ('Task', 'Task'), ('Sub Task', 'Sub Task')], default='Task', max_length=30)),
                ('assigned_to', models.ForeignKey(blank=True, default='admin', null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('project', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='projects.project')),
            ],
        ),
    ]
