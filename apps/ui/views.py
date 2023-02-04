from django.shortcuts import render
from django.views import View

from apps.projects.models import Project


class IndexView(View):
    def get(self, request):
        project_qs = Project.objects.filter(members__in=[request.user], is_active=True)
        return render(request, "ui/index.html", {'project_qs': project_qs})
