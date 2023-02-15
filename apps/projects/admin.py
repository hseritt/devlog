from django.contrib import admin

from apps.core.admin import NoDeleteModelAdmin
from .models import Project


class ProjectAdmin(NoDeleteModelAdmin):
    pass


admin.site.register(Project, ProjectAdmin)
