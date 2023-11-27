from rest_framework import viewsets
from jogs.models import JoggingRecord, CustomUser
from jogs.serializers import JoggingRecordSerializer, CustomUserSerializer, SignUpSerializer
from jogs.permissions import IsOwnerOrReadOnly, IsUserManager, IsAdmin
from rest_framework import permissions


class JoggingRecordViewSet(viewsets.ModelViewSet):
    queryset = JoggingRecord.objects.all()
    serializer_class = JoggingRecordSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]

    def get_permissions(self):
        if self.action == 'create':
            return [permissions.IsAuthenticated()]
        if self.action in ['update', 'partial_update', 'destroy']:
            return [IsOwnerOrReadOnly()]
        return [permissions.IsAuthenticatedOrReadOnly()]

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


class CustomUserViewSet(viewsets.ModelViewSet):
    queryset = CustomUser.objects.all()
    serializer_class = CustomUserSerializer

    def get_queryset(self):
        user = self.request.user

        if user.is_authenticated:

            if user.role in ['admin', 'user_manager']:
                return CustomUser.objects.all().order_by('id')
            else:
                return CustomUser.objects.filter(id=user.id).order_by('id')
        else:
            return CustomUser.objects.none()


class SignUpViewSet(viewsets.ModelViewSet):
    queryset = CustomUser.objects.none()
    serializer_class = SignUpSerializer
