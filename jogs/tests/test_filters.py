from rest_framework import status
from rest_framework.test import APITestCase
from rest_framework.reverse import reverse_lazy
from accounts.models import User
from django.utils import timezone
from jogs.models import JoggingRecord


class TestDynamicFilter(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.client.force_authenticate(user=self.user)

        JoggingRecord.objects.create(owner=self.user, date=timezone.now().date(), time=timezone.timedelta(minutes=30),
                                     distance=5, location='Tbilisi')
        JoggingRecord.objects.create(owner=self.user, date=timezone.now().date(), time=timezone.timedelta(minutes=45),
                                     distance=8, location='London')
        JoggingRecord.objects.create(owner=self.user, date=timezone.now().date(), time=timezone.timedelta(minutes=60),
                                     distance=7, location='Batumi')

    def test_dynamic_filter_backend(self):
        endpoint = reverse_lazy("jogging-records-list")

        response = self.client.get(endpoint, {"q": "distance gt 4"})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['count'], 3)

        response = self.client.get(endpoint, {"q": "location eq London"})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['count'], 1)

        response = self.client.get(endpoint, {"q": "time gt 800 "})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['count'], 3)

        response = self.client.get(endpoint, {"q": "date eq 2024-02-08"})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['count'], 3)
