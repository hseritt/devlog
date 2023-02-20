from django import forms
from django.forms import DateTimeInput, ModelForm
from apps.projects.models import Project
from apps.tasks.models import Task, Comment
from apps.tasks.models import Task, Comment, Category
from apps.sprints.models import Sprint


class AddTaskForm(ModelForm):
    """
    A form for creating a new task.

    Fields:
        subject: A required char field for the task subject.

    Excluded Fields:
        assigned_to: The user who is assigned to the task.
        project: The project that the task belongs to.
        sprint: The sprint that the task is associated with.
        blocked_by_tasks: Tasks that are blocking this task.
        cloned_by_tasks: Tasks that were cloned from this task.
        related_to_tasks: Tasks that are related to this task.
        blocking_tasks: Tasks that are blocked by this task.
        status: The status of the task.
        date_closed: The date when the task was closed.
    """

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
            "last_action_by",
        ]


class AddCommentForm(ModelForm):
    """
    A form for adding a new comment to a task.

    Excluded Fields:
        task: The task that the comment is associated with.
        author: The user who posted the comment.
    """

    class Meta:
        model = Comment
        exclude = [
            "task",
            "author",
        ]


class UpdateTaskForm(ModelForm):
    """
    A form for updating an existing task.

    Fields:
        subject: A required char field for the task subject.

    Excluded Fields:
        project: The project that the task belongs to.
        date_closed: The date when the task was closed.
    """

    subject = forms.CharField(max_length=100)

    class Meta:
        model = Task
        exclude = [
            "project",
            "date_closed",
            "last_action_by",
        ]


class AddSprintForm(ModelForm):
    """
    A form for creating a new sprint.

    Excluded Fields:
        None

    Widgets:
        started: A datetime widget for selecting the sprint start time.
        end: A datetime widget for selecting the sprint end time.

    Args:
        user: The user who is creating the sprint.
    """

    def __init__(self, *args, **kwargs):
        user = kwargs.pop("user", None)
        status = kwargs.pop("status", None)
        super(AddSprintForm, self).__init__(*args, **kwargs)
        if user:
            self.fields["leader"].initial = user.id
            self.fields["project"].queryset = Project.objects.filter(members__in=[user])
        if status:
            self.fields["status"].choices = (("Future", "Future"),)
            self.fields[
                "status"
            ].help_text = "No open sprints can be created if there are any sprints currently open."

    class Meta:
        model = Sprint
        exclude = []
        widgets = {
            "started": DateTimeInput(attrs={"type": "datetime-local"}),
            "end": DateTimeInput(attrs={"type": "datetime-local"}),
        }


class UpdateSprintForm(ModelForm):
    """
    A form for updating an existing sprint.

    Fields:
        status: A required field for the sprint status.

    Excluded Fields:
        None

    Args:
        None
    """

    status_choices = (
        ("Open", "Open"),
        ("Ended", "Ended"),
    )
    status = forms.ChoiceField(choices=status_choices)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Limit the choices based on some condition
        limit_choices = ["Open", "Ended"]
        self.fields["status"].choices = [
            c for c in self.fields["status"].choices if c[0] in limit_choices
        ]

    class Meta:
        model = Sprint
        exclude = []


class AddCategoryForm(ModelForm):
    class Meta:
        model = Category
        exclude = ["project"]
