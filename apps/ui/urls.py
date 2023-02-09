from django.contrib.auth.decorators import login_required
from django.urls import path
from .views import (
    IndexView,
    ProjectView,
    SprintView,
    AddTaskToSprintView,
    RemoveTaskFromSprintView,
    AddTaskView,
    TaskView,
    AddCommentView,
    UpdateTaskView,
    AddSprintView,
    UpdateSprintView,
)

urlpatterns = [
    path("", login_required(IndexView.as_view()), name="ui-index-view"),
    path(
        "project/<int:project_id>/",
        login_required(ProjectView.as_view()),
        name="ui-project-view",
    ),
    path(
        "sprint/<int:sprint_id>/",
        login_required(SprintView.as_view()),
        name="ui-sprint-view",
    ),
    path(
        "sprint/<int:sprint_id>/task/<int:task_id>/addto/",
        login_required(AddTaskToSprintView.as_view()),
        name="ui-add-task-to-sprint-view",
    ),
    path(
        "sprint/<int:sprint_id>/task/<int:task_id>/remove/",
        login_required(RemoveTaskFromSprintView.as_view()),
        name="ui-remove-task-from-sprint-view",
    ),
    path(
        "project/<int:project_id>/task/add/",
        login_required(AddTaskView.as_view()),
        name="ui-add-task-view",
    ),
    path(
        "task/<int:task_id>/", login_required(TaskView.as_view()), name="ui-task-view"
    ),
    path(
        "task/<int:task_id>/comment/add/",
        login_required(AddCommentView.as_view()),
        name="ui-add-comment-view",
    ),
    path(
        "task/<int:task_id>/update/",
        login_required(UpdateTaskView.as_view()),
        name="ui-update-task-view",
    ),
    path(
        "sprint/add/",
        login_required(AddSprintView.as_view()),
        name="ui-add-sprint-view",
    ),
    path(
        "sprint/<int:sprint_id>/update/",
        login_required(UpdateSprintView.as_view()),
        name="ui-update-sprint-view",
    ),
]
