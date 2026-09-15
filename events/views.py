from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render

from matching.models import Match

from .forms import EventForm
from .models import Event


@login_required
def propose_event(request, match_id):
    my_dog = request.user.owner.dogs.first()
    match = get_object_or_404(Match, id=match_id)

    if my_dog.id not in (match.dog_one_id, match.dog_two_id):
        return redirect('matching:match_list')

    other_dog = match.other_dog(my_dog)

    if request.method == 'POST':
        form = EventForm(request.POST)
        if form.is_valid():
            event = form.save(commit=False)
            event.match = match
            event.proposed_by = my_dog
            event.save()
            return redirect('matching:match_list')
    else:
        form = EventForm()

    return render(request, 'events/propose.html', {'form': form, 'other_dog': other_dog})


@login_required
def respond_event(request, event_id):
    my_dog = request.user.owner.dogs.first()
    event = get_object_or_404(Event, id=event_id)

    if my_dog.id == event.proposed_by_id:
        return redirect('matching:match_list')

    if request.method == 'POST':
        decision = request.POST.get('decision')
        if decision == 'confirmar':
            event.status = Event.Status.CONFIRMADO
            event.save()
        elif decision == 'recusar':
            event.status = Event.Status.RECUSADO
            event.save()

    return redirect('matching:match_list')