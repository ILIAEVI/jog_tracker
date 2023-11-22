from rest_framework import serializers
from jogs.models import JoggingRecord
from django.contrib.auth.models import User


class JoggingRecordSerializer(serializers.HyperlinkedModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.username')

    class Meta:
        model = JoggingRecord
        fields = ['id', 'owner', 'created', 'date', 'time', 'distance', 'location', 'weather_condition']


class UserSerializer(serializers.HyperlinkedModelSerializer):
    jogs = serializers.HyperlinkedRelatedField(many=True, view_name='jogging-record-detail', read_only=True)

    class Meta:
        model = User
        fields = ['id', 'username', 'jogs']

