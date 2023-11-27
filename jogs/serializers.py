from rest_framework import serializers
from jogs.models import JoggingRecord, CustomUser


class JoggingRecordSerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.username')
    weather_condition = serializers.ReadOnlyField()

    class Meta:
        model = JoggingRecord
        fields = ['id', 'owner', 'created', 'date', 'time', 'distance', 'location', 'weather_condition']


class CustomUserSerializer(serializers.ModelSerializer):
    jogs = serializers.PrimaryKeyRelatedField(many=True, queryset=JoggingRecord.objects.all())
    role = serializers.ReadOnlyField()

    class Meta:
        model = CustomUser
        fields = ['id', 'username', 'jogs', 'role']


class SignUpSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True, style={'input_type': 'password'})
    role = serializers.ReadOnlyField()

    class Meta:
        model = CustomUser
        fields = ['id', 'username', 'password', 'role']

    def create(self, validated_data):
        user = CustomUser.objects.create_user(**validated_data)
        return user
