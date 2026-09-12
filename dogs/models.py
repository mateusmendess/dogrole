from django.db import models

from accounts.models import Owner


class Dog(models.Model):
    class Size(models.TextChoices):
        PEQUENO = 'P', 'Pequeno'
        MEDIO = 'M', 'Médio'
        GRANDE = 'G', 'Grande'

    class EnergyLevel(models.TextChoices):
        BAIXA = 'baixa', 'Baixa'
        MEDIA = 'media', 'Média'
        ALTA = 'alta', 'Alta'

    class Sociability(models.TextChoices):
        BAIXA = 'baixa', 'Baixa'
        MEDIA = 'media', 'Média'
        ALTA = 'alta', 'Alta'

    owner = models.ForeignKey(Owner, on_delete=models.CASCADE, related_name='dogs')
    name = models.CharField(max_length=100)
    breed = models.CharField(max_length=100, blank=True)
    size = models.CharField(max_length=1, choices=Size.choices)
    energy_level = models.CharField(max_length=10, choices=EnergyLevel.choices)
    sociability = models.CharField(max_length=10, choices=Sociability.choices)
    age = models.PositiveIntegerField(help_text='Idade em anos')
    wants_playdate = models.BooleanField(default=True)
    wants_breeding = models.BooleanField(default=False)
    photo = models.ImageField(upload_to='dogs/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name