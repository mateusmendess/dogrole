from .models import Match, Swipe
from dogs.models import Dog


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


SIZE_ORDER = {
    Dog.Size.PEQUENO: 0,
    Dog.Size.MEDIO: 1,
    Dog.Size.GRANDE: 2,
}

LEVEL_ORDER = {
    'baixa': 0,
    'media': 1,
    'alta': 2,
}


def _ordinal_score(value_a, value_b, order_map, max_points):
    diff = abs(order_map[value_a] - order_map[value_b])
    max_diff = max(order_map.values())
    return max_points * (1 - diff / max_diff)


def compatibility_score(dog_a, dog_b):
    size_points = _ordinal_score(dog_a.size, dog_b.size, SIZE_ORDER, max_points=25)
    energy_points = _ordinal_score(dog_a.energy_level, dog_b.energy_level, LEVEL_ORDER, max_points=25)
    sociability_points = _ordinal_score(dog_a.sociability, dog_b.sociability, LEVEL_ORDER, max_points=30)

    age_diff = abs(dog_a.age - dog_b.age)
    age_points = max(0, 20 - age_diff * 4)

    return size_points + energy_points + sociability_points + age_points