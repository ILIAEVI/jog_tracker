from django.db import models
from django.contrib.auth.models import User


class JoggingRecord(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)
    date = models.DateField()
    time = models.DurationField()
    distance = models.FloatField()
    location = models.CharField(max_length=255)
    weather_condition = models.CharField(max_length=255, null=True, blank=True)

    class Meta:
        ordering = ['created']
