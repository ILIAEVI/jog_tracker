from django.db import models
from django.contrib.auth.models import User, AbstractUser
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
from django.core.validators import MinValueValidator
from jogs.utils import get_weather_condition


def validate_positive_duration(value):
    if value.total_seconds() <= 0:
        raise ValidationError(
            _('Duration must be a positive value.'),
            code='invalid'
        )


class CustomUser(AbstractUser):
    USER_ROLE = [
        ('regular', 'Regular User'),
        ('user_manager', 'User Manager'),
        ('admin', 'Admin'),
    ]

    role = models.CharField(max_length=255, choices=USER_ROLE, default='regular')


class JoggingRecord(models.Model):
    owner = models.ForeignKey(CustomUser, related_name='jogs', on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)
    date = models.DateField()
    time = models.DurationField(validators=[validate_positive_duration])
    distance = models.FloatField(validators=[MinValueValidator(0)])
    location = models.CharField(max_length=255)
    weather_condition = models.CharField(max_length=255, null=True, blank=True)

    class Meta:
        ordering = ['created']

    def save(self, *args, **kwargs):
        api_key = '58f6ef66d7384bf8bc690701232511'
        weather_conditions = get_weather_condition(api_key, self.date, self.location)

        self.weather_condition = weather_conditions

        super().save(*args, **kwargs)
