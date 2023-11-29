from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated

from jogs.models import JoggingRecord
from jogs.serializers import JoggingRecordSerializer
from jogs.permissions import IsOwnerOrReadOnly
from rest_framework import permissions


class JoggingRecordViewSet(viewsets.ModelViewSet):
    queryset = JoggingRecord.objects.all()
    serializer_class = JoggingRecordSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]

    def get_permissions(self):
        if self.action == 'create':
            return [IsAuthenticated()]
        elif self.action in ['update', 'partial_update', 'destroy']:
            return [IsOwnerOrReadOnly()]

        return [permissions.IsAuthenticatedOrReadOnly(), IsOwnerOrReadOnly()]

    def get_queryset(self):
        user = self.request.user

        if user.is_authenticated:
            if user.role == 'admin':
                return JoggingRecord.objects.all()
            else:
                return JoggingRecord.objects.filter(owner=user)
        else:
            return JoggingRecord.objects.none()

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)
