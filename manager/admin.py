from django.contrib import admin
from .models import Task, TaskType, Position, Worker


@admin.register(TaskType)
class TaskTypeAdmin(admin.ModelAdmin):
    list_display = ("id", "name")
    search_fields = ("name",)


@admin.register(Position)
class PositionAdmin(admin.ModelAdmin):
    list_display = ("id", "name")
    search_fields = ("name",)


@admin.register(Worker)
class WorkerAdmin(admin.ModelAdmin):
    list_display = ("id", "username", "email", "position")
    list_filter = ("position",)
    search_fields = ("username", "first_name", "last_name", "email")


@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "priority", "deadline", "is_completed", "task_type")
    list_filter = ("priority", "task_type", "is_completed")
    search_fields = ("name", "description")
    filter_horizontal = ("assignees",)
