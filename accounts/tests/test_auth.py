from rest_framework import status
from rest_framework.test import APITestCase
from rest_framework.reverse import reverse_lazy
from accounts.models import User


class AuthenticationTest(APITestCase):

    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpassword', email='test@example.com')
        self.admin_user = User.objects.create_superuser(username='testadmin', password='adminpassword',
                                                        email='admin@example.com')
        self.user_manager = User.objects.create_user(username='testusermanager', password='managerpass',
                                                     email='manager@example.com', role='user_manager')

    def test_signup(self):
        endpoint = reverse_lazy("users-signup")
        data = {"username": "newuser", "email": "new@gmail.com", "password": "newpassword", "password2": "newpassword"}
        response = self.client.post(endpoint, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(User.objects.count(), 4)

    def test_login_invalid_data(self):
        endpoint = reverse_lazy("users-login")
        data = {"username": "username", "password": "password"}
        response = self.client.post(endpoint, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_user_login_logout(self):
        endpoint = reverse_lazy("users-login")
        data = {"username": "testuser", "password": "testpassword"}
        response = self.client.post(endpoint, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue("token" in response.data)
        self.token = response.data["token"]

        logout_endpoint = reverse_lazy("users-logout")
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token)
        response = self.client.post(logout_endpoint)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_user_update_role(self):
        login_endpoint = reverse_lazy("users-login")
        data = {"username": "testadmin", "password": "adminpassword"}
        response = self.client.post(login_endpoint, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue("token" in response.data)
        token = response.data["token"]
        endpoint = reverse_lazy("users-update-role", kwargs={"pk": self.user.id})
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + token)
        data = {"role": "user_manager"}
        response = self.client.patch(endpoint, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        updated_user = User.objects.get(pk=self.user.id)
        self.assertEqual(updated_user.role, "user_manager")

    def test_get_all_users(self):
        endpoint = reverse_lazy("users-login")
        data = {"username": "testusermanager", "password": "managerpass"}
        response = self.client.post(endpoint, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue("token" in response.data)
        token = response.data["token"]
        url = reverse_lazy("users-list")
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + token)
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
