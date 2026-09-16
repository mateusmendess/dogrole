from .models import Subscription

DAILY_FREE_LIKE_LIMIT = 10


def can_like(owner, likes_today):
    subscription, _ = Subscription.objects.get_or_create(owner=owner)
    if subscription.is_paid:
        return True
    return likes_today < DAILY_FREE_LIKE_LIMIT