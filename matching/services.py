from .models import Match, Swipe


def register_swipe(from_dog, to_dog, liked):
    swipe, created = Swipe.objects.get_or_create(
        from_dog=from_dog,
        to_dog=to_dog,
        defaults={'liked': liked},
    )

    if not created or not liked:
        return swipe, None

    reciprocal = Swipe.objects.filter(
        from_dog=to_dog,
        to_dog=from_dog,
        liked=True,
    ).exists()

    if reciprocal:
        match = Match.objects.create(dog_one=from_dog, dog_two=to_dog)
        return swipe, match

    return swipe, None