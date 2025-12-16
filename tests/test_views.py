from django.test import TestCase
from django.urls import reverse
from django.utils import timezone

from manager.models import Task, TaskType, Position, Worker


class LoggedInTestCase(TestCase):
    def setUp(self):
        self.position = Position.objects.create(name="Developer")
        self.user = Worker.objects.create_user(
            username="testuser",
            password="password123",
            position=self.position,
        )
        self.client.login(username="testuser", password="password123")


class IndexViewTest(LoggedInTestCase):
    def test_index_view_status_code(self):
        response = self.client.get(reverse("manager:index"))
        self.assertEqual(response.status_code, 200)

    def test_index_view_context(self):
        response = self.client.get(reverse("manager:index"))
        self.assertIn("num_tasks", response.context)
        self.assertIn("num_workers", response.context)
        self.assertIn("num_positions", response.context)


class TaskTypeViewsTest(LoggedInTestCase):
    def setUp(self):
        super().setUp()
        self.task_type = TaskType.objects.create(name="Bug")

    def test_task_type_list_view(self):
        response = self.client.get(reverse("manager:task-type-list"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Bug")

    def test_task_type_create_view(self):
        response = self.client.post(
            reverse("manager:task-type-create"),
            {"name": "Feature"},
        )
        self.assertEqual(response.status_code, 302)
        self.assertTrue(TaskType.objects.filter(name="Feature").exists())


class TaskViewsTest(LoggedInTestCase):
    def setUp(self):
        super().setUp()
        self.task_type = TaskType.objects.create(name="Bug")

        self.task = Task.objects.create(
            name="Fix login bug",
            description="Login page error",
            deadline=timezone.now(),
            priority=Task.Priority.HIGH,
            task_type=self.task_type,
        )
        self.task.assignees.add(self.user)

    def test_task_list_view(self):
        response = self.client.get(reverse("manager:task-list"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.task.name)

    def test_task_detail_view(self):
        response = self.client.get(
            reverse("manager:task-detail", args=[self.task.id])
        )
        self.assertEqual(response.status_code, 200)

    def test_task_create_view(self):
        response = self.client.post(
            reverse("manager:task-create"),
            {
                "name": "New task",
                "description": "Test description",
                "deadline": timezone.now(),
                "priority": Task.Priority.MEDIUM,
                "task_type": self.task_type.id,
                "assignees": [self.user.id],
            },
        )
        self.assertEqual(response.status_code, 302)
        self.assertTrue(Task.objects.filter(name="New task").exists())


