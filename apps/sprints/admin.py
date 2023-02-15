from django.contrib import admin
from django.forms import ModelForm, inlineformset_factory
from markdownx.admin import MarkdownxModelAdmin
from apps.core.admin import NoDeleteModelAdmin
from apps.tasks.models import Task
from .models import Sprint


class TaskForm(ModelForm):
    class Meta:
        model = Task
        exclude = ("sprint",)  # exclude the foreign key field


TaskModelInlineFormSet = inlineformset_factory(
    Sprint,
    Task,
    form=TaskForm,
    extra=0,  # don't show extra blank forms
    can_delete=False,  # don't allow deletion of existing records
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


class SprintAdmin(NoDeleteModelAdmin):
    inlines = [TasksInline]
    show_delete_link = False


admin.site.register(Sprint, SprintAdmin)
