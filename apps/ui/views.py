from django.shortcuts import render
from django.views import View

from apps.projects.models import Project


class IndexView(View):
    template = "ui/index.html"

    def get(self, request):
        project_qs = Project.objects.filter(members__in=[request.user], is_active=True)
        return render(request, self.template, {"project_qs": project_qs})


class ProjectView(View):
    template = "ui/project.html"

    def get(self, request, project_id):
        project = Project.objects.get(
            pk=project_id, members__in=[request.user], is_active=True
        )
        return render(request, self.template, {"project": project})
