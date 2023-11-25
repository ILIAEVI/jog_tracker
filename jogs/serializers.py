from rest_framework import serializers
from jogs.models import JoggingRecord
from django.contrib.auth.models import User


class JoggingRecordSerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.username')
    weather_condition = serializers.ReadOnlyField()

    class Meta:
        model = JoggingRecord
        fields = ['id', 'owner', 'created', 'date', 'time', 'distance', 'location', 'weather_condition']


class UserSerializer(serializers.ModelSerializer):
    jogs = serializers.PrimaryKeyRelatedField(many=True, queryset=JoggingRecord.objects.all())

    class Meta:
        model = User
        fields = ['id', 'username', 'jogs']


class SignUpSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True, style={'input_type': 'password'})

    class Meta:
        model = User
        fields = ['id', 'username', 'password']

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        return user
