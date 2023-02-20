from django.contrib import admin
from markdownx.admin import MarkdownxModelAdmin
from apps.core.admin import NoDeleteModelAdmin
from .models import Task, Comment, Category
from .forms import CategoryAdminForm


class CommentsInline(admin.TabularInline):
    model = Comment
    show_change_link = True
    exclude = []
    can_delete = False
    extra = 0


@admin.register(Task)
class TaskAdmin(MarkdownxModelAdmin, NoDeleteModelAdmin):
    inlines = [CommentsInline]


@admin.register(Comment)
class CommentAdmin(MarkdownxModelAdmin):
    pass


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    form = CategoryAdminForm
