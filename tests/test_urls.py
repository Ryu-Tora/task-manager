from django.test import SimpleTestCase
from django.urls import reverse, resolve
from manager.views import TaskListView, index


class UrlsTest(SimpleTestCase):
    def test_index_url_resolves(self):
        url = reverse("manager:index")
        self.assertEqual(resolve(url).func, index)

    def test_task_list_url_resolves(self):
        url = reverse("manager:task-list")
        self.assertEqual(resolve(url).func.view_class, TaskListView)
