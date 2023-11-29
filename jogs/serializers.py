from rest_framework import serializers
from jogs.models import JoggingRecord


class JoggingRecordSerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.username')
    weather_condition = serializers.ReadOnlyField()

    class Meta:
        model = JoggingRecord
        fields = ['id', 'owner', 'created', 'date', 'time', 'distance', 'location', 'weather_condition']
