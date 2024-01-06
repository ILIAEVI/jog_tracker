from rest_framework import serializers
from jogs.models import JoggingRecord, WeeklyReport


class JoggingRecordSerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.username')
    weather_condition = serializers.ReadOnlyField()

    class Meta:
        model = JoggingRecord
        fields = ['id', 'owner', 'created', 'date', 'time', 'distance', 'location', 'weather_condition']


class WeeklyReportSerializer(serializers.ModelSerializer):
    class Meta:
        model = WeeklyReport
        fields = ['id', 'user', 'start_date', 'end_date', 'avg_speed', 'total_distance']