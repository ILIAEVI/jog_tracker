from django.urls import path, include
from rest_framework.routers import DefaultRouter
from jogs.views import JoggingRecordViewSet, UserViewSet, SignUpViewSet


router = DefaultRouter()
router.register(r'jogging-records', JoggingRecordViewSet, basename='jogging-record')
router.register(r'users', UserViewSet, basename='user')
router.register(r'signups', SignUpViewSet, basename='signup')

urlpatterns = [
    path('', include(router.urls)),
]

urlpatterns += [
    path('api-auth/', include('rest_framework.urls')),
]
