from django.contrib.auth.models import User
from django.test import TestCase

from accounts.models import Owner

from .models import Subscription
from .services import DAILY_FREE_LIKE_LIMIT, can_like


class CanLikeTest(TestCase):
    def setUp(self):
        user = User.objects.create_user(username='dono', password='senha123')
        self.owner = Owner.objects.create(user=user, city='São Luís')

    def test_creates_free_subscription_automatically(self):
        self.assertFalse(Subscription.objects.filter(owner=self.owner).exists())
        can_like(self.owner, likes_today=0)
        subscription = Subscription.objects.get(owner=self.owner)
        self.assertEqual(subscription.plan, Subscription.Plan.GRATUITO)

    def test_free_plan_blocks_after_limit(self):
        self.assertTrue(can_like(self.owner, likes_today=DAILY_FREE_LIKE_LIMIT - 1))
        self.assertFalse(can_like(self.owner, likes_today=DAILY_FREE_LIKE_LIMIT))

    def test_paid_plan_has_no_limit(self):
        Subscription.objects.create(owner=self.owner, plan=Subscription.Plan.PAGO)
        self.assertTrue(can_like(self.owner, likes_today=9999))