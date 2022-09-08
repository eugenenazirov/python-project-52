from django.contrib.auth.models import User
from django.test import TestCase, Client
from django.urls import reverse


class TestUser(TestCase):
    def setUp(self):
        self.client = Client()

        user = User.objects.create(username='test_user', first_name="Alexander")
        user.set_password('12345')
        user.save()

    def test_user_list_without_auth(self):
        response = self.client.get(reverse('users_list'))
        assert response.status_code == 200

    def test_creating_user(self):
        self.client.post(reverse('users_create'), {
            'username': 'EuNaz',
            'first_name': 'Eugene',
            'last_name': 'Nazirov',
            'password1': 'pss12asddaSA',
            'password2': 'pss12asddaSA'
        })
        user = User.objects.get(id=2)
        assert user.username == "EuNaz"

    def test_updating_user(self):
        self.client.login(username='test_user', password='12345')

        self.client.post(reverse('users_update', args=[1]), {
            'username': 'DarNaz',
            'first_name': 'Darya',
            'last_name': 'Naz',
            'password1': 'pss12asddaSA',
            'password2': 'pss12asddaSA'
        })

        user = User.objects.get(id=1)
        assert user.first_name == "Darya"

    def test_updating_user_without_auth(self):
        response = self.client.post(reverse('users_update', args=[1]), {
            'username': 'EuNaz',
            'first_name': 'Eugene',
            'last_name': 'Nazirov',
            'password1': 'pss12asddaSA',
            'password2': 'pss12asddaSA'
        })

        user = User.objects.get(id=1)

        assert response.url == "/login/"
        assert response.status_code == 302
        assert user.first_name == "Eugene"

    def test_deleting_user(self):
        self.client.login(username='test_user', password='12345')
        self.client.post(reverse('users_delete', args=[1]))
        users = User.objects.all().count()
        assert users == 0

    def test_deleting_user_without_auth(self):
        response = self.client.post(reverse('users_delete', args=[1]))
        users = User.objects.all().count()
        assert response.url == "/login/"
        assert response.status_code == 302
        assert users == 1
