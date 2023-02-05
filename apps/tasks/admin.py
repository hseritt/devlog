from django.contrib import admin
from .models import Task, Comment, Category
from .forms import CategoryAdminForm


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


class CategoryAdmin(admin.ModelAdmin):
    form = CategoryAdminForm


admin.site.register(Task, TaskAdmin)
admin.site.register(Comment)
admin.site.register(Category, CategoryAdmin)
