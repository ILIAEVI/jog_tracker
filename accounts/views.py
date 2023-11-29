from django.contrib.auth import authenticate, login, logout
from rest_framework import status
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from accounts.serializers import UserSerializer, SignUpSerializer, RoleUpdateSerializer, LogInSerializer
from accounts.models import User
from rest_framework.authtoken.models import Token
from accounts.permissions import IsAdminOrReadOnly


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def get_queryset(self):
        user = self.request.user

        if user.is_authenticated:

            if user.role in ['admin', 'user_manager']:
                return User.objects.all().order_by('id')
            else:
                return User.objects.filter(id=user.id).order_by('id')
        else:
            return User.objects.none()

    @action(
        methods=("put", "patch"),
        detail=True,
        url_path='update-role',
        serializer_class=RoleUpdateSerializer,
        permission_classes=[IsAuthenticated, IsAdminOrReadOnly]
    )
    def update_role(self, request, pk):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(status=status.HTTP_204_NO_CONTENT)

    @action(detail=False, methods=['post'], url_path='signup', serializer_class=SignUpSerializer)
    def signup(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    @action(detail=False, methods=['post'], url_path='login', serializer_class=LogInSerializer)
    def login(self, request):
        username = request.data.get('username')
        password = request.data.get('password')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            token, _ = Token.objects.get_or_create(user=user)
            return Response({'token': token.key})
        else:
            return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)

    @action(detail=False, methods=['post'], url_path='logout')
    def logout(self, request):
        user = self.request.user
        if user.is_authenticated:
            logout(request)
            Token.objects.filter(user=user).delete()
            return Response({'success': 'Successfully logged out'})
        else:
            return Response({'error': 'User not authenticated'}, status=status.HTTP_401_UNAUTHORIZED)
