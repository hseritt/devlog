# Generated by Django 3.2.17 on 2023-02-14 23:53

from django.db import migrations
import markdownx.models


class Migration(migrations.Migration):

    dependencies = [
        ('sprints', '0003_alter_sprint_status'),
    ]

    operations = [
        migrations.AddField(
            model_name='sprint',
            name='description',
            field=markdownx.models.MarkdownxField(blank=True, null=True),
        ),
    ]