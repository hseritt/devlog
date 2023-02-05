from django.contrib.auth.decorators import login_required
from django.urls import path
from .views import IndexView, ProjectView

urlpatterns = [
    path("", login_required(IndexView.as_view()), name="ui-index-view"),
    path(
        "project/<int:project_id>",
        login_required(ProjectView.as_view()),
        name="ui-project-view",
    ),
]
