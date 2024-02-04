from django.urls import path, include
from rest_framework.routers import DefaultRouter
from jogs.views import JoggingRecordViewSet, WeeklyReportViewSet


router = DefaultRouter()
router.register(r'jogging-records', JoggingRecordViewSet, basename='jogging-records')
router.register(r'weekly-reports', WeeklyReportViewSet, basename='weekly-reports')

urlpatterns = [
    path('', include(router.urls)),
]
