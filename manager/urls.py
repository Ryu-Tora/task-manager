from django.urls import path

from manager.views import index, PositionListView, TaskListView, TaskTypeListView, WorkerListView

urlpatterns = [
    path("", index, name="index"),
    path(
        "positions/",
        PositionListView.as_view(),
        name="position-list"
    ),
    path(
        "tasks/",
        TaskListView.as_view(),
        name="task-list"
    ),
    path("task_types/",
        TaskTypeListView.as_view(),
        name="task-type-list"
    ),
    path("workers/",
        WorkerListView.as_view(),
        name="worker-list"
    ),
    ]
