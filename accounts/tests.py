from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse

from .models import Owner


class OwnerModelTest(TestCase):
    def test_str_returns_username(self):
        user = User.objects.create_user(username='mateus', password='senha123')
        owner = Owner.objects.create(user=user, city='São Luís')
        self.assertEqual(str(owner), 'mateus')


class SignupViewTest(TestCase):
    def test_get_renders_form(self):
        response = self.client.get(reverse('accounts:signup'))
        self.assertEqual(response.status_code, 200)

    def test_post_creates_user_and_owner_and_logs_in(self):
        data = {
            'username': 'novodono',
            'email': 'novo@exemplo.com',
            'password': 'senha123',
            'city': 'São Luís',
            'phone': '',
        }
        response = self.client.post(reverse('accounts:signup'), data)
        self.assertRedirects(response, reverse('accounts:home'))
        self.assertTrue(User.objects.filter(username='novodono').exists())
        user = User.objects.get(username='novodono')
        self.assertTrue(Owner.objects.filter(user=user).exists())
        self.assertIn('_auth_user_id', self.client.session)


class LoginLogoutTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='mateus', password='senha123')
        Owner.objects.create(user=self.user, city='São Luís')

    def test_login_with_correct_credentials(self):
        response = self.client.post(reverse('accounts:login'), {
            'username': 'mateus',
            'password': 'senha123',
        })
        self.assertRedirects(response, reverse('accounts:home'))
        self.assertIn('_auth_user_id', self.client.session)

    def test_login_with_wrong_password_fails(self):
        response = self.client.post(reverse('accounts:login'), {
            'username': 'mateus',
            'password': 'senhaerrada',
        })
        self.assertEqual(response.status_code, 200)
        self.assertNotIn('_auth_user_id', self.client.session)

    def test_logout_ends_session(self):
        self.client.login(username='mateus', password='senha123')
        response = self.client.get(reverse('accounts:logout'))
        self.assertRedirects(response, reverse('accounts:login'))
        self.assertNotIn('_auth_user_id', self.client.session)