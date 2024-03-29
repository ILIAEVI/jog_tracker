from django.db import models
from accounts.models import User
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
from django.core.validators import MinValueValidator
from jogs.utils import get_weather_condition
import environ


env = environ.Env()


def validate_positive_duration(value):
    if value.total_seconds() <= 0:
        raise ValidationError(
            _('Duration must be a positive value.'),
            code='invalid'
        )


class JoggingRecord(models.Model):
    owner = models.ForeignKey(User, related_name='jogs', on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)
    date = models.DateField()
    time = models.DurationField(validators=[validate_positive_duration])
    distance = models.FloatField(validators=[MinValueValidator(0)])
    location = models.CharField(max_length=255)
    weather_condition = models.JSONField(max_length=255, null=True, blank=True)

    class Meta:
        ordering = ['created']

    def save(self, *args, **kwargs):
        api_key = env('API_KEY')
        weather_conditions = get_weather_condition(api_key, self.date, self.location)

        self.weather_condition = weather_conditions

        super().save(*args, **kwargs)


class WeeklyReport(models.Model):
    owner = models.ForeignKey(User, related_name='weekly_reports', on_delete=models.CASCADE)
    start_date = models.DateField()
    end_date = models.DateField()
    avg_speed = models.FloatField(default=0)
    total_distance = models.FloatField(default=0)

    class Meta:
        ordering = ['owner', 'start_date']
