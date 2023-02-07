from django.db.models import Q
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.views import View

from apps.projects.models import Project
from apps.sprints.models import Sprint
from apps.tasks.models import Task

from .forms import AddTaskForm, AddCommentForm, UpdateTaskForm


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


class SprintView(View):
    template = "ui/sprint.html"

    def get(self, request, sprint_id):
        sprint = Sprint.objects.get(pk=sprint_id, project__members__in=[request.user])
        return render(request, self.template, {"sprint": sprint})


class AddTaskToSprintView(View):
    def get(self, request, sprint_id, task_id):
        sprint = Sprint.objects.get(pk=sprint_id)
        task = Task.objects.get(pk=task_id)
        task.sprint = sprint
        task.save()
        return HttpResponseRedirect(
            reverse(
                "ui-sprint-view",
                args=[
                    sprint.id,
                ],
            )
        )


class RemoveTaskFromSprintView(View):
    def get(self, request, sprint_id, task_id):
        task = Task.objects.get(pk=task_id)
        task.sprint = None
        task.save()

        return HttpResponseRedirect(
            reverse(
                "ui-sprint-view",
                args=[
                    sprint_id,
                ],
            )
        )


class AddTaskView(View):
    template = "ui/add_task.html"

    def get(self, request, project_id):
        project = Project.objects.get(pk=project_id)
        add_task_form = AddTaskForm()
        return render(
            request,
            self.template,
            context={"project": project, "add_task_form": add_task_form},
        )

    def post(self, request, project_id):
        project = Project.objects.get(pk=project_id)
        add_task_form = AddTaskForm(request.POST)
        if add_task_form.is_valid():
            task = add_task_form.save(commit=False)
            task.project = project
            task.save()
            add_task_form.save_m2m()

            return HttpResponseRedirect(
                reverse(
                    "ui-project-view",
                    args=[
                        project.id,
                    ],
                )
            )
        print("IT WAS NOT VALID.")
        return render(
            request,
            self.template,
            context={"project": project, "add_task_form": add_task_form},
        )


class TaskView(View):
    template = "ui/task.html"

    def get(self, request, task_id):
        task = Task.objects.get(pk=task_id, project__members__in=[request.user])
        return render(request, self.template, {"task": task})


class AddCommentView(View):
    template = "ui/add_comment.html"

    def get(self, request, task_id):
        task = Task.objects.get(pk=task_id)
        add_comment_form = AddCommentForm()
        return render(
            request,
            self.template,
            context={"task": task, "add_comment_form": add_comment_form},
        )

    def post(self, request, task_id):
        task = Task.objects.get(pk=task_id)
        add_comment_form = AddCommentForm(request.POST)
        if add_comment_form.is_valid():
            comment = add_comment_form.save(commit=False)
            comment.task = task
            comment.author = request.user
            comment.save()

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


class UpdateTaskView(View):
    template = "ui/update_task.html"

    def get(self, request, task_id):
        task = Task.objects.get(pk=task_id)
        update_task_form = UpdateTaskForm(instance=task)
        update_task_form.fields["sprint"].queryset = Sprint.objects.filter(
            status="Open", project=task.project
        )
        update_task_form.fields["blocked_by_tasks"].queryset = Task.objects.exclude(
            Q(status="Closed") | Q(status="Won't Fix")
        )
        update_task_form.fields["cloned_by_tasks"].queryset = Task.objects.exclude(
            Q(status="Closed") | Q(status="Won't Fix")
        )
        update_task_form.fields["related_to_tasks"].queryset = Task.objects.exclude(
            Q(status="Closed") | Q(status="Won't Fix")
        )
        update_task_form.fields["blocking_tasks"].queryset = Task.objects.exclude(
            Q(status="Closed") | Q(status="Won't Fix")
        )
        return render(
            request,
            self.template,
            context={"task": task, "update_task_form": update_task_form},
        )

    def post(self, request, task_id):
        task = Task.objects.get(pk=task_id)
        update_task_form = UpdateTaskForm(request.POST, instance=task)
        if update_task_form.is_valid():
            update_task_form.save()
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
