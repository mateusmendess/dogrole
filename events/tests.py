from datetime import timedelta

from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse
from django.utils import timezone

from accounts.models import Owner
from dogs.models import Dog
from matching.models import Match

from .models import Event


def create_dog(owner, name):
    return Dog.objects.create(
        owner=owner,
        name=name,
        size=Dog.Size.MEDIO,
        energy_level=Dog.EnergyLevel.MEDIA,
        sociability=Dog.Sociability.ALTA,
        age=3,
    )


class ProposeEventViewTest(TestCase):
    def setUp(self):
        owner_a = Owner.objects.create(
            user=User.objects.create_user(username='dono_a', password='senha123'),
            city='São Luís',
        )
        owner_b = Owner.objects.create(
            user=User.objects.create_user(username='dono_b', password='senha123'),
            city='São Luís',
        )
        owner_c = Owner.objects.create(
            user=User.objects.create_user(username='dono_c', password='senha123'),
            city='São Luís',
        )
        self.dog_a = create_dog(owner_a, 'Rex')
        self.dog_b = create_dog(owner_b, 'Bela')
        create_dog(owner_c, 'Totó')
        self.match = Match.objects.create(dog_one=self.dog_a, dog_two=self.dog_b)

    def test_requires_login(self):
        response = self.client.get(reverse('events:propose', args=[self.match.id]))
        self.assertNotEqual(response.status_code, 200)

    def test_dog_outside_match_is_redirected(self):
        self.client.login(username='dono_c', password='senha123')
        response = self.client.get(reverse('events:propose', args=[self.match.id]))
        self.assertRedirects(response, reverse('matching:match_list'))

    def test_post_creates_event(self):
        self.client.login(username='dono_a', password='senha123')
        data = {
            'location': 'Praça da Igrejinha',
            'scheduled_at': '2026-10-01T15:00',
        }
        response = self.client.post(reverse('events:propose', args=[self.match.id]), data)
        self.assertRedirects(response, reverse('matching:match_list'))

        event = Event.objects.get(match=self.match)
        self.assertEqual(event.proposed_by, self.dog_a)
        self.assertEqual(event.location, 'Praça da Igrejinha')
        self.assertEqual(event.status, Event.Status.PENDENTE)


class RespondEventViewTest(TestCase):
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
        match = Match.objects.create(dog_one=self.dog_a, dog_two=self.dog_b)
        self.event = Event.objects.create(
            match=match,
            proposed_by=self.dog_a,
            location='Praça da Igrejinha',
            scheduled_at=timezone.now() + timedelta(days=1),
        )

    def test_proposer_cannot_respond(self):
        self.client.login(username='dono_a', password='senha123')
        self.client.post(reverse('events:respond', args=[self.event.id]), {'decision': 'confirmar'})
        self.event.refresh_from_db()
        self.assertEqual(self.event.status, Event.Status.PENDENTE)

    def test_other_side_can_confirm(self):
        self.client.login(username='dono_b', password='senha123')
        self.client.post(reverse('events:respond', args=[self.event.id]), {'decision': 'confirmar'})
        self.event.refresh_from_db()
        self.assertEqual(self.event.status, Event.Status.CONFIRMADO)

    def test_other_side_can_decline(self):
        self.client.login(username='dono_b', password='senha123')
        self.client.post(reverse('events:respond', args=[self.event.id]), {'decision': 'recusar'})
        self.event.refresh_from_db()
        self.assertEqual(self.event.status, Event.Status.RECUSADO)