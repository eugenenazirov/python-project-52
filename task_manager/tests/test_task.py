from task_manager.models import Status, Task
from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User


class TestTask(TestCase):
    def setUp(self):
        self.client = Client()

        user = User.objects.create(username='test_user')
        user.set_password('12345')
        user.save()

        Status.objects.create(name='test_status')

    def test_access_to_tasks_list(self):
        self.client.login(username='test_user', password='12345')
        response = self.client.get(reverse('tasks_list'))

        assert response.status_code == 200

    def test_access_to_tasks_list_without_auth(self):
        response = self.client.get(reverse('tasks_list'))
        assert response.url == "/login/"
        assert response.status_code == 302

    def test_access_to_tasks_create_without_auth(self):
        response = self.client.get(reverse('tasks_create'))
        assert response.url == "/login/"
        assert response.status_code == 302

        status = Status.objects.get(id=1)
        response = self.client.post(reverse('tasks_create'), {
            'name': 'Task_1',
            'status': status.id,
        })

        tasks = Task.objects.all().count()
        assert tasks == 0
        assert response.url == "/login/"
        assert response.status_code == 302

    def test_create_task(self):
        self.client.login(username='test_user', password='12345')
        status = Status.objects.get(id=1)
        self.client.post(reverse('tasks_create'), {
            'name': 'Task_1',
            'status': status.id,
        })
        task = Task.objects.get(id=1)
        assert task.name == "Task_1"

    def test_update_task(self):
        status = Status.objects.get(id=1)
        user = User.objects.get(id=1)
        Task.objects.create(name='task_1', status=status, author=user)
        self.client.login(username='test_user', password='12345')

        self.client.post(reverse('tasks_update', args=[1]), {
            'name': 'task_2',
            'status': status.id,
        })
        task = Task.objects.get(id=1)

        assert task.name == "task_2"

    def test_update_task_without_auth(self):
        status = Status.objects.get(id=1)
        user = User.objects.get(id=1)
        Task.objects.create(name='task_1', status=status, author=user)

        response = self.client.post(reverse('tasks_update', args=[1]), {
            'name': 'task_2',
            'status': status.id,
        })
        task = Task.objects.get(id=1)

        assert task.name == "task_1"
        assert response.url == "/login/"
        assert response.status_code == 302

        response = self.client.get(reverse('tasks_update', args=[1]))
        assert response.url == "/login/"
        assert response.status_code == 302

    def test_deleting_task(self):
        status = Status.objects.get(id=1)
        user = User.objects.get(id=1)
        Task.objects.create(name='task_1', status=status, author=user)

        self.client.login(username='test_user', password='12345')
        self.client.post(reverse('tasks_delete', args=[1]))
        tasks_count = Task.objects.all().count()
        assert tasks_count == 0

    def test_deleting_task_without_auth(self):
        status = Status.objects.get(id=1)
        user = User.objects.get(id=1)
        Task.objects.create(name='task_1', status=status, author=user)

        response = self.client.post(reverse('tasks_delete', args=[1]))
        tasks_count = Task.objects.all().count()

        assert response.url == "/login/"
        assert response.status_code == 302
        assert tasks_count == 1

        response = self.client.get(reverse('tasks_delete', args=[1]))
        assert response.url == "/login/"
        assert response.status_code == 302

    def test_details_task(self):
        status = Status.objects.get(id=1)
        user = User.objects.get(id=1)
        Task.objects.create(name='task_1', status=status, author=user)

        self.client.login(username='test_user', password='12345')
        response = self.client.get(reverse('tasks_detail', args=[1]))

        assert response.status_code == 200

    def test_details_task_withour_auth(self):
        status = Status.objects.get(id=1)
        user = User.objects.get(id=1)
        Task.objects.create(name='task_1', status=status, author=user)

        response = self.client.get(reverse('tasks_detail', args=[1]))

        assert response.url == "/login/"
        assert response.status_code == 302
