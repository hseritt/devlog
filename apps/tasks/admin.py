from django.contrib import admin
from .models import Task, Comment


class CommentsInline(admin.TabularInline):
    model = Comment
    show_change_link = True
    exclude = []
    can_delete = False
    extra = 0


class TaskAdmin(admin.ModelAdmin):
    inlines = [
        CommentsInline,
    ]


admin.site.register(Task, TaskAdmin)
admin.site.register(Comment)
