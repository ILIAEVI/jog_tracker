from django.utils import timezone
from rest_framework import status
from rest_framework.reverse import reverse_lazy
from rest_framework.test import APITestCase
from accounts.models import User


class WeatherApiTests(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='test', email='test@gmail.com', password='test1')
        self.client.force_authenticate(user=self.user)

    def test_get_weather_condition(self):
        data = {
            "date": timezone.now().date(),
            "time": "3000",
            "distance": "4000",
            "location": "Tbilisi"
        }
        endpoint = reverse_lazy('jogging-records-list')
        response = self.client.post(endpoint, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIn('weather_condition', response.data)
