import datetime

from celery import shared_task
from django.db.models import Avg, Sum
from .models import JoggingRecord, WeeklyReport
from django.utils import timezone
from datetime import timedelta
from accounts.models import User


@shared_task
def generate_weekly_report():
    users = User.objects.all()

    for user in users:
        try:
            today = timezone.now().date()
            start_date = today - timedelta(days=today.weekday())
            end_date = start_date + timedelta(days=6)

            weekly_records = JoggingRecord.objects.filter(owner=user, date__range=[start_date, end_date])

            if weekly_records.exists():
                aggregates = weekly_records.aggregate(
                    sum_distance=Sum('distance'),
                    sum_time=Sum('time')
                )
                sum_time_seconds = aggregates['sum_time'].total_seconds()
                total_distance = aggregates['sum_distance']
                if sum_time_seconds > 0:
                    # Calculate average speed only if sum_time_seconds is positive
                    average_speed = round(total_distance / sum_time_seconds, 3)
                else:
                    average_speed = 0
            else:
                average_speed = 0
                total_distance = 0

            report, created = WeeklyReport.objects.get_or_create(
                owner=user, start_date=start_date, end_date=end_date
            )
            report.avg_speed = average_speed
            report.total_distance = total_distance
            report.save()
        except Exception as e:
            print(f"Error creating/updating weekly report for {user}: {e}")
