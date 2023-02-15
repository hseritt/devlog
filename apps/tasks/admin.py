from django.contrib import admin

from apps.core.admin import NoDeleteModelAdmin
from .models import Task, Comment, Category
from markdownx.admin import MarkdownxModelAdmin
from .forms import CategoryAdminForm


class CommentsInline(admin.TabularInline):
    model = Comment
    show_change_link = True
    exclude = []
    can_delete = False
    extra = 0


class TaskAdmin(MarkdownxModelAdmin, NoDeleteModelAdmin):
    inlines = [
        CommentsInline,
    ]


class CategoryAdmin(admin.ModelAdmin):
    form = CategoryAdminForm


admin.site.register(
    Task,
    TaskAdmin,
)
admin.site.register(Comment, MarkdownxModelAdmin)
admin.site.register(Category, CategoryAdmin)
