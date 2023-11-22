from rest_framework import viewsets
from jogs.models import JoggingRecord
from jogs.serializers import JoggingRecordSerializer, UserSerializer
from django.contrib.auth.models import User
from jogs.permissions import IsOwnerOrReadOnly
from rest_framework import permissions


class JoggingRecordViewSet(viewsets.ModelViewSet):
    queryset = JoggingRecord.objects.all()
    serializer_class = JoggingRecordSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class UserViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
