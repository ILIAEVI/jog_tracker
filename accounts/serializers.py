from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from accounts.models import User
from jogs.models import JoggingRecord


class UserSerializer(serializers.ModelSerializer):
    jogs = serializers.PrimaryKeyRelatedField(many=True, queryset=JoggingRecord.objects.all())
    role = serializers.ReadOnlyField()

    class Meta:
        model = User
        fields = ['id', 'username', 'jogs', 'role']


class RoleUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['role']


class SignUpSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True, style={'input_type': 'password'})
    password2 = serializers.CharField(write_only=True, required=True, style={'input_type': 'password'})
    role = serializers.ReadOnlyField()

    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'password', 'password2', 'role']

    def validate(self, attrs):
        password = attrs['password']
        password2 = attrs['password2']
        if password != password2:
            raise ValidationError("Password doesn't match")

        return attrs

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        return user


class LogInSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'password']

