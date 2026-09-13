from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render

from dogs.models import Dog

from .models import Swipe
from .services import register_swipe


@login_required
def feed(request):
    my_dog = request.user.owner.dogs.first()
    if my_dog is None:
        return redirect('dogs:create')

    match = None

    if request.method == 'POST':
        to_dog = get_object_or_404(Dog, id=request.POST.get('dog_id'))
        liked = request.POST.get('liked') == 'true'
        _, match = register_swipe(my_dog, to_dog, liked)

    already_swiped_ids = Swipe.objects.filter(from_dog=my_dog).values_list('to_dog_id', flat=True)
    next_dog = Dog.objects.exclude(owner=my_dog.owner).exclude(id__in=already_swiped_ids).first()

    return render(request, 'matching/feed.html', {'dog': next_dog, 'match': match})