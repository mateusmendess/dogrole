from django.db import models

from dogs.models import Dog


class Swipe(models.Model):
    from_dog = models.ForeignKey(Dog, related_name='swipes_given', on_delete=models.CASCADE)
    to_dog = models.ForeignKey(Dog, related_name='swipes_received', on_delete=models.CASCADE)
    liked = models.BooleanField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('from_dog', 'to_dog')


class Match(models.Model):
    dog_one = models.ForeignKey(Dog, related_name='matches_as_one', on_delete=models.CASCADE)
    dog_two = models.ForeignKey(Dog, related_name='matches_as_two', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.dog_one.name} + {self.dog_two.name}'