from django.urls import path, include
from rest_framework.routers import DefaultRouter
from jogs.views import JoggingRecordViewSet


router = DefaultRouter()
router.register(r'jogging-records', JoggingRecordViewSet, basename='jogging-record')

urlpatterns = [
    path('', include(router.urls)),
]
