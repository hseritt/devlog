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
    path("", IndexView.as_view(), name="ui-index-view"),
    path(
        "project/<int:project_id>/",
        ProjectView.as_view(),
        name="ui-project-view",
    ),
    path(
        "sprint/<int:sprint_id>/",
        SprintView.as_view(),
        name="ui-sprint-view",
    ),
    path(
        "sprint/<int:sprint_id>/task/<int:task_id>/addto/",
        AddTaskToSprintView.as_view(),
        name="ui-add-task-to-sprint-view",
    ),
    path(
        "sprint/<int:sprint_id>/task/<int:task_id>/remove/",
        RemoveTaskFromSprintView.as_view(),
        name="ui-remove-task-from-sprint-view",
    ),
    path(
        "project/<int:project_id>/task/add/",
        AddTaskView.as_view(),
        name="ui-add-task-view",
    ),
    path("task/<int:task_id>/", TaskView.as_view(), name="ui-task-view"),
    path(
        "task/<int:task_id>/comment/add/",
        AddCommentView.as_view(),
        name="ui-add-comment-view",
    ),
    path(
        "task/<int:task_id>/update/",
        UpdateTaskView.as_view(),
        name="ui-update-task-view",
    ),
    path(
        "sprint/add/",
        AddSprintView.as_view(),
        name="ui-add-sprint-view",
    ),
    path(
        "sprint/<int:sprint_id>/update/",
        UpdateSprintView.as_view(),
        name="ui-update-sprint-view",
    ),
]
