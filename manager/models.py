from django.contrib.auth.models import AbstractUser
from django.db import models


class ModelWithNameFieldMixin(models.Model):
    name = models.CharField(
        max_length=255,
        unique=True,
    )

    class Meta:
        abstract = True

    def __str__(self):
        return self.name


class TaskType(ModelWithNameFieldMixin):
    pass


class Position(ModelWithNameFieldMixin):
    pass


class Worker(AbstractUser):
    position = models.ForeignKey(
        Position,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="workers",
    )

    def __str__(self):
        return f"Username: {self.username}"


class Worker(AbstractUser):
    position = models.ForeignKey(
        Position,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="workers",
    )

    def __str__(self):
        return f"Username: {self.username}"


class Task(models.Model):
    class Priority(models.TextChoices):
        LOW = "LOW", "Low"
        MEDIUM = "MEDIUM", "Medium"
        HIGH = "HIGH", "High"
        URGENT = "URGENT", "Urgent"

    name = models.CharField(max_length=255)
    description = models.TextField()
    deadline = models.DateTimeField()
    is_completed = models.BooleanField(default=False)
    priority = models.CharField(
        max_length=6,
        choices=Priority.choices,
        default=Priority.MEDIUM,
    )

    task_type = models.ForeignKey(
        TaskType,
        on_delete=models.SET_NULL,
        null=True,
        related_name="tasks",
    )

    assignees = models.ManyToManyField(
        Worker,
        related_name="tasks_assigned",
    )

    class Meta:
        ordering = ["priority"]

    def __str__(self):
        return f"{self.name} ({self.get_priority_display()})"
