from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse

from accounts.models import Owner
from .models import Dog


class DogModelTest(TestCase):
    def test_str_returns_name(self):
        user = User.objects.create_user(username='dono', password='senha123')
        owner = Owner.objects.create(user=user, city='São Luís')
        dog = Dog.objects.create(
            owner=owner,
            name='Rex',
            size=Dog.Size.MEDIO,
            energy_level=Dog.EnergyLevel.ALTA,
            sociability=Dog.Sociability.ALTA,
            age=3,
        )
        self.assertEqual(str(dog), 'Rex')


class CreateDogViewTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='dono', password='senha123')
        Owner.objects.create(user=self.user, city='São Luís')

    def test_requires_login(self):
        response = self.client.get(reverse('dogs:create'))
        self.assertNotEqual(response.status_code, 200)

    def test_logged_in_get_renders_form(self):
        self.client.login(username='dono', password='senha123')
        response = self.client.get(reverse('dogs:create'))
        self.assertEqual(response.status_code, 200)

    def test_post_creates_dog_linked_to_owner(self):
        self.client.login(username='dono', password='senha123')
        data = {
            'name': 'Bidu',
            'breed': 'SRD',
            'size': Dog.Size.PEQUENO,
            'energy_level': Dog.EnergyLevel.MEDIA,
            'sociability': Dog.Sociability.ALTA,
            'age': 2,
            'wants_playdate': True,
            'wants_breeding': False,
        }
        response = self.client.post(reverse('dogs:create'), data)
        self.assertRedirects(response, reverse('accounts:home'))
        self.assertTrue(Dog.objects.filter(name='Bidu', owner__user=self.user).exists())