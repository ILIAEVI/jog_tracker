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

        today = timezone.now().date()
        start_date = today - timedelta(days=today.weekday())
        end_date = start_date + timedelta(days=6)

        weekly_records = JoggingRecord.objects.filter(owner=user, date__range=[start_date, end_date])

        if weekly_records.exists():
            aggregates = weekly_records.aggregate(
                avg_distance=Avg('distance'), avg_time=Avg('time'),
                sum_distance=Sum('distance')
            )
            avg_time: datetime.timedelta = aggregates['avg_time']
            average_speed = aggregates['avg_distance'] / avg_time.total_seconds()
            total_distance = aggregates['sum_distance']
        else:
            average_speed = 0
            total_distance = 0

        try:
            report, created = WeeklyReport.objects.get_or_create(user=user, start_date=start_date, end_date=end_date)
            report.avg_speed = average_speed
            report.total_distance = total_distance
            report.save()
        except Exception as e:
            print(f"Error creating/updating weekly report for {user}: {e}")
