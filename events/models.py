from django.db import models

from dogs.models import Dog
from matching.models import Match


class Event(models.Model):
    class Status(models.TextChoices):
        PENDENTE = 'pendente', 'Pendente'
        CONFIRMADO = 'confirmado', 'Confirmado'
        RECUSADO = 'recusado', 'Recusado'

    match = models.ForeignKey(Match, related_name='events', on_delete=models.CASCADE)
    proposed_by = models.ForeignKey(Dog, related_name='events_proposed', on_delete=models.CASCADE)
    location = models.CharField(max_length=255)
    scheduled_at = models.DateTimeField()
    status = models.CharField(max_length=10, choices=Status.choices, default=Status.PENDENTE)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.match} em {self.scheduled_at:%d/%m/%Y %H:%M}'