from django.db.models import Q
from django.http import Http404, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.urls import reverse
from django.views import View
from apps.core.views import CustomLoginRequiredMixin

from apps.projects.models import Project
from apps.sprints.models import Sprint
from apps.tasks.models import Task

from .forms import (
    AddTaskForm,
    AddCommentForm,
    UpdateTaskForm,
    AddSprintForm,
    UpdateSprintForm,
)


class IndexView(CustomLoginRequiredMixin, View):
    template = "ui/index.html"

    def get(self, request):
        project_qs = Project.objects.filter(members__in=[request.user], is_active=True)
        return render(request, self.template, {"project_qs": project_qs})


class ProjectView(CustomLoginRequiredMixin, View):
    template = "ui/project.html"

    def get(self, request, project_id):
        project = get_object_or_404(
            Project, pk=project_id, members__in=[request.user], is_active=True
        )
        return render(request, self.template, {"project": project})


class SprintView(CustomLoginRequiredMixin, View):
    template = "ui/sprint.html"

    def get(self, request, sprint_id):
        sprint = get_object_or_404(
            Sprint,
            pk=sprint_id,
            project__members__in=[request.user],
            project__is_active=True,
        )
        return render(request, self.template, {"sprint": sprint})


class AddTaskToSprintView(CustomLoginRequiredMixin, View):
    redirect_url = "ui-sprint-view"

    def get_sprint(self, id):
        return get_object_or_404(
            Sprint,
            pk=id,
            project__members__in=[self.request.user],
            project__is_active=True,
        )

    def get_task(self, id):
        return get_object_or_404(
            Task,
            pk=id,
            project__members__in=[self.request.user],
            project__is_active=True,
        )

    def set_task_sprint(self, task, sprint):
        task.sprint = sprint
        task.save()

    def get_view_objects(self, sprint_id, task_id):
        return self.get_sprint(sprint_id), self.get_task(task_id)

    def get(self, request, sprint_id, task_id):
        self.request = request
        sprint, task = self.get_view_objects(sprint_id, task_id)
        self.set_task_sprint(task, sprint)
        return HttpResponseRedirect(
            reverse(
                self.redirect_url,
                args=[
                    sprint.id,
                ],
            )
        )


class RemoveTaskFromSprintView(CustomLoginRequiredMixin, View):
    def remove_task(self, task_id):
        task = get_object_or_404(
            Task,
            pk=task_id,
            project__members__in=[self.request.user],
            project__is_active=True,
        )
        task.sprint = None
        task.save()

    def get(self, request, sprint_id, task_id):
        self.request = request
        self.remove_task(task_id)
        return HttpResponseRedirect(
            reverse(
                "ui-sprint-view",
                args=[
                    sprint_id,
                ],
            )
        )


class AddTaskView(CustomLoginRequiredMixin, View):
    template = "ui/add_task.html"

    def get(self, request, project_id):
        sprint_id = request.GET.get("sprint", None)
        sprint = Sprint.objects.get(pk=sprint_id) if sprint_id else None
        project = get_object_or_404(
            Project,
            pk=project_id,
            members__in=[request.user],
            is_active=True,
        )
        add_task_form = AddTaskForm()
        return render(
            request,
            self.template,
            context={
                "project": project,
                "add_task_form": add_task_form,
                "sprint": sprint,
            },
        )

    def save_task(self, form, project, request, sprint=None):
        task = form.save(commit=False)
        task.project = project
        task.last_action_by = request.user
        if sprint:
            task.sprint = sprint
        task.save()
        form.save_m2m()

    def post(self, request, project_id):
        sprint_id = request.GET.get("sprint", None)
        sprint = Sprint.objects.get(pk=sprint_id) if sprint_id else None
        project = get_object_or_404(
            Project,
            pk=project_id,
            members__in=[request.user],
            is_active=True,
        )
        add_task_form = AddTaskForm(request.POST)
        if add_task_form.is_valid():
            self.save_task(add_task_form, project, request, sprint=sprint)
            return HttpResponseRedirect(
                reverse(
                    "ui-project-view",
                    args=[
                        project.id,
                    ],
                )
            )
        return render(
            request,
            self.template,
            context={"project": project, "add_task_form": add_task_form},
        )


class TaskView(CustomLoginRequiredMixin, View):
    template = "ui/task.html"

    def get(self, request, task_id):
        task = get_object_or_404(Task, pk=task_id, project__members__in=[request.user])
        return render(request, self.template, {"task": task})


class AddCommentView(CustomLoginRequiredMixin, View):
    template = "ui/add_comment.html"

    def get(self, request, task_id):
        task = get_object_or_404(
            Task,
            pk=task_id,
            project__members__in=[request.user],
            project__is_active=True,
        )
        add_comment_form = AddCommentForm()
        return render(
            request,
            self.template,
            context={"task": task, "add_comment_form": add_comment_form},
        )

    def save_comment(self, form, task, user):
        comment = form.save(commit=False)
        comment.task = task
        comment.author = user
        comment.save()

    def post(self, request, task_id):
        task = get_object_or_404(
            Task,
            pk=task_id,
            project__members__in=[request.user],
            project__is_active=True,
        )
        add_comment_form = AddCommentForm(request.POST)
        if add_comment_form.is_valid():
            self.save_comment(add_comment_form, task, request.user)
            return HttpResponseRedirect(
                reverse(
                    "ui-task-view",
                    args=[
                        task.id,
                    ],
                )
            )
        return render(
            request,
            self.template,
            context={"task": task, "add_comment_form": add_comment_form},
        )


class UpdateTaskView(CustomLoginRequiredMixin, View):
    template = "ui/update_task.html"

    def set_form_querysets(self, form, task):
        fields_exclude_closed = (
            "blocked_by_tasks",
            "cloned_by_tasks",
            "related_to_tasks",
            "blocking_tasks",
        )

        form.fields["sprint"].queryset = Sprint.objects.filter(
            status="Open",
            project=task.project,
            project__members__in=[self.request.user],
            project__is_active=True,
        )

        for field in fields_exclude_closed:
            form.fields[field].queryset = Task.objects.exclude(
                Q(status="Closed") | Q(status="Won't Fix"),
                project__members__in=[self.request.user],
                project__is_active=True,
            )

    def get(self, request, task_id):
        self.request = request
        task = get_object_or_404(
            Task,
            pk=task_id,
            project__members__in=[self.request.user],
            project__is_active=True,
        )
        update_task_form = UpdateTaskForm(instance=task)
        self.set_form_querysets(update_task_form, task)
        return render(
            request,
            self.template,
            context={"task": task, "update_task_form": update_task_form},
        )

    def post(self, request, task_id):
        self.request = request
        task = get_object_or_404(
            Task,
            pk=task_id,
            project__members__in=[self.request.user],
            project__is_active=True,
        )
        update_task_form = UpdateTaskForm(request.POST, instance=task)
        if update_task_form.is_valid():
            task = update_task_form.save(commit=False)
            task.last_action_by = request.user
            task.save()
            return HttpResponseRedirect(
                reverse(
                    "ui-task-view",
                    args=[
                        task_id,
                    ],
                )
            )
        return render(
            request,
            self.template,
            context={"task": task, "update_task_form": update_task_form},
        )


def check_project_membership(user):
    user_projects = Project.objects.filter(members=user)
    if not user_projects.exists():
        raise Http404(
            "User is not a member of any project. User must be a member of a project in order to access this page."
        )


class AddSprintView(CustomLoginRequiredMixin, View):
    template = "ui/add_sprint.html"

    def get(self, request):
        check_project_membership(request.user)
        add_sprint_form = AddSprintForm(user=request.user)
        return render(
            request,
            self.template,
            context={"add_sprint_form": add_sprint_form},
        )

    def post(self, request):
        check_project_membership(request.user)
        add_sprint_form = AddSprintForm(request.POST, user=request.user)
        if add_sprint_form.is_valid():
            sprint = add_sprint_form.save()
            return HttpResponseRedirect(
                reverse(
                    "ui-sprint-view",
                    args=[
                        sprint.id,
                    ],
                )
            )
        return render(
            request,
            self.template,
            context={"add_sprint_form": add_sprint_form},
        )


class UpdateSprintView(CustomLoginRequiredMixin, View):
    template = "ui/update_sprint.html"

    def get(self, request, sprint_id):
        sprint = get_object_or_404(
            Sprint,
            pk=sprint_id,
            project__members__in=[request.user],
            project__is_active=True,
        )
        update_sprint_form = UpdateSprintForm(instance=sprint)
        return render(
            request,
            self.template,
            context={"sprint": sprint, "update_sprint_form": update_sprint_form},
        )

    def post(self, request, sprint_id):
        sprint = get_object_or_404(
            Sprint,
            pk=sprint_id,
            project__members__in=[request.user],
            project__is_active=True,
        )
        update_sprint_form = UpdateSprintForm(request.POST, instance=sprint)
        if update_sprint_form.is_valid():
            update_sprint_form.save()
            return HttpResponseRedirect(
                reverse(
                    "ui-sprint-view",
                    args=[
                        sprint.id,
                    ],
                )
            )
        return render(
            request,
            self.template,
            context={"sprint": sprint, "update_sprint_form": update_sprint_form},
        )
