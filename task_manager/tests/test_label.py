from task_manager.models import Label
from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User


class TestLabel(TestCase):
    def setUp(self):
        self.client = Client()

        user = User.objects.create(username='test_user')
        user.set_password('12345')
        user.save()

    def test_access_to_labels_list(self):
        self.client.login(username='test_user', password='12345')
        response = self.client.get(reverse('labels_list'))
        assert response.status_code == 200

    def test_access_to_labels_list_without_auth(self):
        response = self.client.get(reverse('labels_list'))
        assert response.url == "/login/"
        assert response.status_code == 302

    def test_creating_label(self):
        self.client.login(username='test_user', password='12345')
        self.client.post(reverse('labels_create'), {
            'name': 'label_1'
        })
        label = Label.objects.get(id=1)
        assert label.name == "label_1"

    def test_creating_label_without_auth(self):
        response = self.client.post(reverse('labels_create'), {
            'name': 'label_1'
        })
        labels = Label.objects.all().count()
        assert labels == 0
        assert response.url == "/login/"
        assert response.status_code == 302

        response = self.client.get(reverse('labels_create'))
        assert response.url == "/login/"
        assert response.status_code == 302

    def test_updating_label(self):
        Label.objects.create(name='label_1')
        self.client.login(username='test_user', password='12345')
        self.client.post(reverse('labels_update', args=[1]), {
            'name': 'label_2'
        })

        label = Label.objects.get(id=1)
        assert label.name == "label_2"

    def test_updating_label_without_auth(self):
        Label.objects.create(name='label_1')
        response = self.client.post(reverse('labels_update', args=[1]), {
            'name': 'label_2'
        })

        label = Label.objects.get(id=1)
        assert response.url == "/login/"
        assert response.status_code == 302
        assert label.name == "label_1"

        response = self.client.get(reverse('labels_update', args=[1]))
        assert response.url == "/login/"
        assert response.status_code == 302

    def test_deleting_label(self):
        Label.objects.create(name='label_1')
        self.client.login(username='test_user', password='12345')
        self.client.post(reverse('labels_delete', args=[1]))
        label_count = Label.objects.all().count()
        assert label_count == 0

    def test_deleting_label_without_auth(self):
        Label.objects.create(name='label_1')
        response = self.client.post(reverse('labels_delete', args=[1]))
        label_count = Label.objects.all().count()
        assert label_count == 1
        assert response.url == "/login/"
        assert response.status_code == 302

        response = self.client.get(reverse('labels_delete', args=[1]))
        assert response.url == "/login/"
        assert response.status_code == 302
