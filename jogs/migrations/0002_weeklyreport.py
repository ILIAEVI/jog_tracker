# Generated by Django 4.2.7 on 2024-01-06 14:23

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('jogs', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='WeeklyReport',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('start_date', models.DateField()),
                ('end_date', models.DateField()),
                ('avg_speed', models.FloatField(default=0)),
                ('total_distance', models.FloatField(default=0)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='weekly_reports', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ['user', 'start_date'],
            },
        ),
    ]
