from django.db import models

from accounts.models import Owner


class Subscription(models.Model):
    class Plan(models.TextChoices):
        GRATUITO = 'gratuito', 'Gratuito'
        PAGO = 'pago', 'Pago'

    owner = models.OneToOneField(Owner, related_name='subscription', on_delete=models.CASCADE)
    plan = models.CharField(max_length=10, choices=Plan.choices, default=Plan.GRATUITO)
    mercadopago_subscription_id = models.CharField(max_length=100, blank=True)
    active_until = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.owner} - {self.get_plan_display()}'

    @property
    def is_paid(self):
        return self.plan == self.Plan.PAGO