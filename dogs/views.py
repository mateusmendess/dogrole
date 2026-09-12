from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render

from .forms import DogForm


@login_required
def create_dog(request):
    if request.method == 'POST':
        form = DogForm(request.POST, request.FILES)
        if form.is_valid():
            dog = form.save(commit=False)
            dog.owner = request.user.owner
            dog.save()
            return redirect('accounts:home')
    else:
        form = DogForm()
    return render(request, 'dogs/create.html', {'form': form})