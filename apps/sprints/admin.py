from django.contrib import admin
from django.forms import ModelForm, inlineformset_factory
from markdownx.admin import MarkdownxModelAdmin
from apps.core.admin import NoDeleteModelAdmin
from apps.tasks.models import Task
from .models import Sprint


class TaskForm(ModelForm):
    class Meta:
        model = Task
        exclude = ("sprint",)


TaskModelInlineFormSet = inlineformset_factory(
    Sprint,
    Task,
    form=TaskForm,
    extra=0,
    can_delete=False,
)


class TasksInline(admin.TabularInline):
    model = Task
    formset = TaskModelInlineFormSet
    extra = 0
    show_change_link = False
    exclude = [
        "description",
        "blocked_by_tasks",
        "cloned_by_tasks",
        "blocking_tasks",
        "related_to_tasks",
        "categories",
        "project",
        "type",
    ]
    can_delete = False
    max_num = 0


@admin.register(Sprint)
class SprintAdmin(NoDeleteModelAdmin, MarkdownxModelAdmin):
    inlines = [TasksInline]
    show_delete_link = False
