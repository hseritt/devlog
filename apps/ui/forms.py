from django import forms
from django.forms import ModelForm
from apps.tasks.models import Task, Comment
from apps.sprints.models import Sprint


class AddTaskForm(ModelForm):
    subject = forms.CharField(max_length=100)

    class Meta:
        model = Task
        exclude = [
            "assigned_to",
            "project",
            "sprint",
            "blocked_by_tasks",
            "cloned_by_tasks",
            "related_to_tasks",
            "blocking_tasks",
            "status",
            "date_closed",
        ]


class AddCommentForm(ModelForm):
    class Meta:
        model = Comment
        exclude = [
            "task",
            "author",
        ]


class UpdateTaskForm(ModelForm):
    subject = forms.CharField(max_length=100)

    class Meta:
        model = Task
        exclude = [
            "project",
            "date_closed",
        ]


class AddSprintForm(ModelForm):
    class Meta:
        model = Sprint
        exclude = []


class UpdateSprintForm(ModelForm):
    class Meta:
        model = Sprint
        exclude = []
