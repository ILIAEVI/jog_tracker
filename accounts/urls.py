from django.urls import path, include
from rest_framework.routers import DefaultRouter
from accounts.views import UserViewSet


router = DefaultRouter()
router.register(r'users', UserViewSet, basename='users')

urlpatterns = [
    path('', include(router.urls)),
]

urlpatterns += [
    path('api-auth/', include('rest_framework.urls')),
]
