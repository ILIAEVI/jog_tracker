from rest_framework import status
from rest_framework.test import APITestCase
from rest_framework.reverse import reverse_lazy
from accounts.models import User
from django.utils import timezone

from jogs.models import JoggingRecord


class TestCrudRegularUser(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='test', email='test@gmail.com', password='test')
        endpoint = reverse_lazy("users-login")
        data = {"username": "test", "password": "test"}
        response = self.client.post(endpoint, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue("token" in response.data)
        self.token = response.data["token"]
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token)

    def test_create_record(self):
        endpoint = reverse_lazy("jogging-records-list")
        data = {"date": timezone.now().date(), "time": "3000", "distance": "4000", "location": "Tbilisi"}
        response = self.client.post(endpoint, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_update_record(self):
        endpoint = reverse_lazy("jogging-records-list")
        data = {"date": timezone.now().date(), "time": "3000", "distance": "4000", "location": "Tbilisi"}
        response = self.client.post(endpoint, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue("id" in response.data)
        self.id = response.data["id"]

        update_endpoint = reverse_lazy("jogging-records-detail", args=[self.id])
        data = {"time": "4000"}
        response = self.client.patch(update_endpoint, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_delete_record(self):
        endpoint = reverse_lazy("jogging-records-list")
        data = {"date": timezone.now().date(), "time": "3000", "distance": "4000", "location": "Tbilisi"}
        response = self.client.post(endpoint, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue("id" in response.data)
        self.id = response.data["id"]

        delete_endpoint = reverse_lazy("jogging-records-detail", args=[self.id])
        response = self.client.delete(delete_endpoint, format='json')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)


class TestAdminCrud(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpassword', email='test@example.com')
        self.client.force_authenticate(user=self.user)

        self.record1 = JoggingRecord.objects.create(owner=self.user, date=timezone.now().date(),
                                                    time=timezone.timedelta(minutes=30), distance=5, location='Tbilisi')
        self.record2 = JoggingRecord.objects.create(owner=self.user, date=timezone.now().date(),
                                                    time=timezone.timedelta(minutes=45), distance=8, location='London')
        self.client.force_authenticate(user=None)
        self.admin = User.objects.create_superuser(username="admin", email="admin@gmail.com", password="admin1")
        endpoint = reverse_lazy("users-login")
        data = {"username": "admin", "password": "admin1"}
        response = self.client.post(endpoint, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue("token" in response.data)
        self.token = response.data["token"]
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token)

    def test_create_record(self):
        endpoint = reverse_lazy("jogging-records-list")
        data = {"date": timezone.now().date(), "time": "3000", "distance": "4000", "location": "Batumi"}
        response = self.client.post(endpoint, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_update_record(self):
        self.id = self.record1.id
        update_endpoint = reverse_lazy("jogging-records-detail", args=[self.id])
        data = {"time": "4000"}
        response = self.client.patch(update_endpoint, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_delete_record(self):
        self.id = self.record1.id
        delete_endpoint = reverse_lazy("jogging-records-detail", args=[self.id])
        response = self.client.delete(delete_endpoint, format='json')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        