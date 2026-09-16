from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse

from accounts.models import Owner
from dogs.models import Dog
from subscriptions.services import DAILY_FREE_LIKE_LIMIT

from .models import Match, Swipe
from .services import compatibility_score, register_swipe


def create_dog(owner, name, **kwargs):
    fields = {
        'size': Dog.Size.MEDIO,
        'energy_level': Dog.EnergyLevel.MEDIA,
        'sociability': Dog.Sociability.ALTA,
        'age': 3,
    }
    fields.update(kwargs)
    return Dog.objects.create(owner=owner, name=name, **fields)


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


class CompatibilityScoreTest(TestCase):
    def setUp(self):
        self.owner_a = Owner.objects.create(
            user=User.objects.create_user(username='dono_a', password='senha123'),
            city='São Luís',
        )
        self.owner_b = Owner.objects.create(
            user=User.objects.create_user(username='dono_b', password='senha123'),
            city='São Luís',
        )

    def test_identical_dogs_score_maximum(self):
        dog_a = create_dog(self.owner_a, 'Rex')
        dog_b = create_dog(self.owner_b, 'Bela')
        self.assertEqual(compatibility_score(dog_a, dog_b), 100)

    def test_very_different_dogs_score_zero(self):
        dog_a = create_dog(
            self.owner_a, 'Rex',
            size=Dog.Size.PEQUENO,
            energy_level=Dog.EnergyLevel.BAIXA,
            sociability=Dog.Sociability.BAIXA,
            age=1,
        )
        dog_b = create_dog(
            self.owner_b, 'Bela',
            size=Dog.Size.GRANDE,
            energy_level=Dog.EnergyLevel.ALTA,
            sociability=Dog.Sociability.ALTA,
            age=10,
        )
        self.assertEqual(compatibility_score(dog_a, dog_b), 0)


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
        self.dog_b = create_dog(owner_b, 'Bela', energy_level=Dog.EnergyLevel.ALTA)

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

    def test_feed_shows_most_compatible_dog_first(self):
        owner_c = Owner.objects.create(
            user=User.objects.create_user(username='dono_c', password='senha123'),
            city='São Luís',
        )
        dog_c = create_dog(owner_c, 'Totó')

        self.client.login(username='dono_a', password='senha123')
        response = self.client.get(reverse('matching:feed'))

        self.assertEqual(response.context['dog'], dog_c)


class MatchListViewTest(TestCase):
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
        response = self.client.get(reverse('matching:match_list'))
        self.assertNotEqual(response.status_code, 200)

    def test_lists_match_with_other_dog(self):
        Match.objects.create(dog_one=self.dog_a, dog_two=self.dog_b)

        self.client.login(username='dono_a', password='senha123')
        response = self.client.get(reverse('matching:match_list'))

        other_dogs = [item['other_dog'] for item in response.context['matches']]
        self.assertEqual(other_dogs, [self.dog_b])

    def test_no_matches_shows_empty_list(self):
        self.client.login(username='dono_a', password='senha123')
        response = self.client.get(reverse('matching:match_list'))
        self.assertEqual(list(response.context['matches']), [])


class FeedLikeLimitTest(TestCase):
    def setUp(self):
        owner_a = Owner.objects.create(
            user=User.objects.create_user(username='dono_a', password='senha123'),
            city='São Luís',
        )
        self.dog_a = create_dog(owner_a, 'Rex')

        for i in range(DAILY_FREE_LIKE_LIMIT):
            owner = Owner.objects.create(
                user=User.objects.create_user(username=f'dono_{i}', password='senha123'),
                city='São Luís',
            )
            dog = create_dog(owner, f'Cao{i}')
            Swipe.objects.create(from_dog=self.dog_a, to_dog=dog, liked=True)

        owner_extra = Owner.objects.create(
            user=User.objects.create_user(username='dono_extra', password='senha123'),
            city='São Luís',
        )
        self.extra_dog = create_dog(owner_extra, 'Totó')

    def test_blocks_like_after_daily_limit(self):
        self.client.login(username='dono_a', password='senha123')
        response = self.client.post(
            reverse('matching:feed'), {'dog_id': self.extra_dog.id, 'liked': 'true'}
        )
        self.assertTrue(response.context['limit_reached'])
        self.assertFalse(
            Swipe.objects.filter(from_dog=self.dog_a, to_dog=self.extra_dog).exists()
        )

    def test_dislike_is_not_blocked_by_limit(self):
        self.client.login(username='dono_a', password='senha123')
        response = self.client.post(
            reverse('matching:feed'), {'dog_id': self.extra_dog.id, 'liked': 'false'}
        )
        self.assertFalse(response.context['limit_reached'])
        self.assertTrue(
            Swipe.objects.filter(from_dog=self.dog_a, to_dog=self.extra_dog, liked=False).exists()
        )