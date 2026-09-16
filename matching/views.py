from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.shortcuts import get_object_or_404, redirect, render

from dogs.models import Dog
from subscriptions.services import can_like

from .models import Match, Swipe
from .services import compatibility_score, register_swipe, todays_likes_count


@login_required
def feed(request):
    my_dog = request.user.owner.dogs.first()
    if my_dog is None:
        return redirect('dogs:create')

    match = None
    limit_reached = False

    if request.method == 'POST':
        liked = request.POST.get('liked') == 'true'
        if liked and not can_like(my_dog.owner, todays_likes_count(my_dog)):
            limit_reached = True
        else:
            to_dog = get_object_or_404(Dog, id=request.POST.get('dog_id'))
            _, match = register_swipe(my_dog, to_dog, liked)

    already_swiped_ids = Swipe.objects.filter(from_dog=my_dog).values_list('to_dog_id', flat=True)
    candidates = Dog.objects.exclude(owner=my_dog.owner).exclude(id__in=already_swiped_ids)
    next_dog = max(candidates, key=lambda dog: compatibility_score(my_dog, dog), default=None)

    return render(request, 'matching/feed.html', {
        'dog': next_dog,
        'match': match,
        'limit_reached': limit_reached,
    })


@login_required
def match_list(request):
    my_dog = request.user.owner.dogs.first()
    if my_dog is None:
        return redirect('dogs:create')
    matches = Match.objects.filter(
        Q(dog_one=my_dog) | Q(dog_two=my_dog)
    ).select_related('dog_one', 'dog_two')
    matches_with_other_dog = [
        {'match': match, 'other_dog': match.other_dog(my_dog), 'events': match.events.all()}
        for match in matches
    ]
    return render(request, 'matching/match_list.html', {'matches': matches_with_other_dog, 'my_dog': my_dog})