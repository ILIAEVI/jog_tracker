from django.test import TestCase
from accounts.models import User
from django.utils import timezone
from rest_framework.test import APIRequestFactory
from jogs.filters import DynamicFilterBackend, build_query_from_dynamic
from jogs.models import JoggingRecord
class DynamicFilterTestCase(TestCase):
    def setUp(self):
        # Create a user
        self.user = User.objects.create_user(username='testuser', password='testpassword')

        # Create some jogging records
        JoggingRecord.objects.create(owner=self.user, date=timezone.now().date(), time=timezone.timedelta(minutes=30), distance=5.0, location='Park')
        JoggingRecord.objects.create(owner=self.user, date=timezone.now().date(), time=timezone.timedelta(minutes=45), distance=7.5, location='Gym')
        JoggingRecord.objects.create(owner=self.user, date=timezone.now().date(), time=timezone.timedelta(minutes=60), distance=10.0, location='Beach')

    def test_dynamic_filter_backend(self):
        factory = APIRequestFactory()

        # Use GET parameters instead of query_params
        request = factory.get('/jogging-records/', {'q': 'distance eq 7.5'})
        queryset = JoggingRecord.objects.all()
        view = None
        filter_backend = DynamicFilterBackend()

        filtered_queryset = filter_backend.filter_queryset(request, queryset, view)
        self.assertEqual(filtered_queryset.count(), 1)
        self.assertEqual(filtered_queryset.first().distance, 7.5)

    def test_build_query_from_dynamic(self):
        # Test the build_query_from_dynamic function with various inputs

        # Example: Test for 'eq' operator
        query_string = 'distance eq 7.5'
        query = build_query_from_dynamic(query_string)
        self.assertTrue(query)
        # Add assertions based on the expected behavior of your filter

        # Example: Test for 'and' operator
        query_string = 'distance eq 5.0 and location eq Park'
        query = build_query_from_dynamic(query_string)
        self.assertTrue(query)
        # Add assertions based on the expected behavior of your filter

        # Add more test cases for other operators and combinations

