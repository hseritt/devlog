from django.contrib import admin
from markdownx.admin import MarkdownxModelAdmin
from apps.tasks.models import Task
from .models import Sprint


class TasksInline(admin.TabularInline):
    model = Task
    show_change_link = True
    exclude = ["description"]
    can_delete = False
    extra = 0


class SprintAdmin(MarkdownxModelAdmin):
    inlines = [
        TasksInline,
    ]


admin.site.register(Sprint, SprintAdmin)
