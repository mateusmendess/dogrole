from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse

from accounts.models import Owner
from dogs.models import Dog

from .models import Match, Swipe
from .services import register_swipe


def create_dog(owner, name):
    return Dog.objects.create(
        owner=owner,
        name=name,
        size=Dog.Size.MEDIO,
        energy_level=Dog.EnergyLevel.MEDIA,
        sociability=Dog.Sociability.ALTA,
        age=3,
    )


class RegisterSwipeTest(TestCase):
    def setUp(self):
        owner_a = Owner.objects.create(
            user=User.objects.create_user(username='dono_a', password='senha123'),
            city='São Luís',
        )
        owner_b = Owner.objects.create(
            user=User.objects.create_user(username='dono_b', password='senha123'),
            city='São Luís',
        )
        self.dog_a = create_dog(owner_a, 'Rex')
        self.dog_b = create_dog(owner_b, 'Bela')

    def test_one_sided_like_does_not_create_match(self):
        _, match = register_swipe(self.dog_a, self.dog_b, True)
        self.assertIsNone(match)
        self.assertEqual(Match.objects.count(), 0)

    def test_mutual_like_creates_match(self):
        register_swipe(self.dog_a, self.dog_b, True)
        _, match = register_swipe(self.dog_b, self.dog_a, True)
        self.assertIsNotNone(match)
        self.assertEqual(Match.objects.count(), 1)

    def test_repeated_swipe_does_not_duplicate(self):
        register_swipe(self.dog_a, self.dog_b, True)
        register_swipe(self.dog_a, self.dog_b, True)
        self.assertEqual(Swipe.objects.count(), 1)


class FeedViewTest(TestCase):
    def setUp(self):
        owner_a = Owner.objects.create(
            user=User.objects.create_user(username='dono_a', password='senha123'),
            city='São Luís',
        )
        owner_b = Owner.objects.create(
            user=User.objects.create_user(username='dono_b', password='senha123'),
            city='São Luís',
        )
        self.dog_a = create_dog(owner_a, 'Rex')
        self.dog_b = create_dog(owner_b, 'Bela')

    def test_requires_login(self):
        response = self.client.get(reverse('matching:feed'))
        self.assertNotEqual(response.status_code, 200)

    def test_shows_other_owners_dog(self):
        self.client.login(username='dono_a', password='senha123')
        response = self.client.get(reverse('matching:feed'))
        self.assertEqual(response.context['dog'], self.dog_b)

    def test_post_like_registers_swipe(self):
        self.client.login(username='dono_a', password='senha123')
        self.client.post(reverse('matching:feed'), {'dog_id': self.dog_b.id, 'liked': 'true'})
        self.assertTrue(
            Swipe.objects.filter(from_dog=self.dog_a, to_dog=self.dog_b, liked=True).exists()
        )