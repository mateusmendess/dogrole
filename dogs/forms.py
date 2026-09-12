from django import forms

from .models import Dog


class DogForm(forms.ModelForm):
    class Meta:
        model = Dog
        fields = [
            'name', 'breed', 'size', 'energy_level', 'sociability',
            'age', 'wants_playdate', 'wants_breeding', 'photo',
        ]