from rest_framework import viewsets
from jogs.models import JoggingRecord
from jogs.serializers import JoggingRecordSerializer, UserSerializer, SignUpSerializer
from django.contrib.auth.models import User
from jogs.permissions import IsOwnerOrReadOnly
from rest_framework import permissions


class JoggingRecordViewSet(viewsets.ModelViewSet):
    queryset = JoggingRecord.objects.all()
    serializer_class = JoggingRecordSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class SignUpViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = SignUpSerializer
