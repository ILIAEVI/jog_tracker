# Generated by Django 4.2.7 on 2023-11-29 12:01

from django.conf import settings
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion
import jogs.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='JoggingRecord',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('date', models.DateField()),
                ('time', models.DurationField(validators=[jogs.models.validate_positive_duration])),
                ('distance', models.FloatField(validators=[django.core.validators.MinValueValidator(0)])),
                ('location', models.CharField(max_length=255)),
                ('weather_condition', models.CharField(blank=True, max_length=255, null=True)),
                ('owner', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='jogs', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ['created'],
            },
        ),
    ]