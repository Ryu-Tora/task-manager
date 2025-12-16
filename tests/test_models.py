from django.test import TestCase
from django.utils import timezone
from django.contrib.auth import get_user_model

from manager.models import (
    TaskType,
    Position,
    Task,
)


class TaskTypeModelTest(TestCase):
    def test_task_type_creation(self):
        task_type = TaskType.objects.create(name="Bug")
        self.assertEqual(task_type.name, "Bug")

    def test_task_type_str(self):
        task_type = TaskType.objects.create(name="Feature")
        self.assertEqual(str(task_type), "Feature")

    def test_task_type_name_unique(self):
        TaskType.objects.create(name="Bug")
        with self.assertRaises(Exception):
            TaskType.objects.create(name="Bug")


class PositionModelTest(TestCase):
    def test_position_creation(self):
        position = Position.objects.create(name="Developer")
        self.assertEqual(position.name, "Developer")

    def test_position_str(self):
        position = Position.objects.create(name="Manager")
        self.assertEqual(str(position), "Manager")


class WorkerModelTest(TestCase):
    def setUp(self):
        self.position = Position.objects.create(name="QA")
        self.worker = get_user_model().objects.create_user(
            username="john_doe",
            password="password123",
            position=self.position,
        )

    def test_worker_creation(self):
        self.assertEqual(self.worker.username, "john_doe")
        self.assertEqual(self.worker.position.name, "QA")

    def test_worker_str(self):
        self.assertEqual(str(self.worker), "Username: john_doe")

    def test_worker_position_nullable(self):
        worker = get_user_model().objects.create_user(
            username="no_position",
            password="password123",
        )
        self.assertIsNone(worker.position)


class TaskModelTest(TestCase):
    def setUp(self):
        self.task_type = TaskType.objects.create(name="Bug")
        self.position = Position.objects.create(name="Developer")

        self.worker1 = get_user_model().objects.create_user(
            username="worker1",
            password="pass123",
            position=self.position,
        )
        self.worker2 = get_user_model().objects.create_user(
            username="worker2",
            password="pass123",
        )

        self.task = Task.objects.create(
            name="Fix login bug",
            description="Login page throws error",
            deadline=timezone.now(),
            priority=Task.Priority.HIGH,
            task_type=self.task_type,
        )
        self.task.assignees.add(self.worker1, self.worker2)


    def test_task_creation(self):
        self.assertEqual(self.task.name, "Fix login bug")
        self.assertEqual(self.task.priority, Task.Priority.HIGH)
        self.assertFalse(self.task.is_completed)
        self.assertEqual(self.task.task_type.name, "Bug")


    def test_task_str(self):
        expected_str = "Fix login bug (High)"
        self.assertEqual(str(self.task), expected_str)


    def test_task_assignees(self):
        assignees = self.task.assignees.all()
        self.assertEqual(assignees.count(), 2)
        self.assertIn(self.worker1, assignees)
        self.assertIn(self.worker2, assignees)


    def test_task_priority_choices(self):
        valid_priorities = [
            Task.Priority.LOW,
            Task.Priority.MEDIUM,
            Task.Priority.HIGH,
            Task.Priority.URGENT,
        ]

        for priority in valid_priorities:
            task = Task.objects.create(
                name=f"Task {priority}",
                description="Test",
                deadline=timezone.now(),
                priority=priority,
                task_type=self.task_type,
            )
            self.assertEqual(task.priority, priority)

    def test_task_default_ordering_by_priority(self):
        low = Task.objects.create(
            name="Low priority",
            description="Test",
            deadline=timezone.now(),
            priority=Task.Priority.LOW,
            task_type=self.task_type,
        )

        urgent = Task.objects.create(
            name="Urgent priority",
            description="Test",
            deadline=timezone.now(),
            priority=Task.Priority.URGENT,
            task_type=self.task_type,
        )

        tasks = list(Task.objects.all())

        self.assertIn(urgent, tasks)
        self.assertIn(low, tasks)
