from django.test import TestCase, Client
from rest_framework import status
from rest_framework.test import APIClient
from rest_framework_simplejwt.tokens import RefreshToken
from django.urls import reverse
from .models import CustomUser, Organization
from .serializers import EventSerializer, CustomUserSerializer


class EventViewTest(TestCase):

    def setUp(self):
        self.client = APIClient()
        self.user = CustomUser.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpassword'
        )
        self.organization = Organization.objects.create(
            title='Test Org',
            address='Test Address',
            postcode='12345'
        )
        self.event_data = {
            'title': 'Test Event',
            'description': 'Event Description',
            'organizations': [self.organization.id],
            'date': '2022-01-01T00:00:00Z',
        }

    def authenticate_user(self):
        refresh = RefreshToken.for_user(self.user)
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {str(refresh.access_token)}')

    def test_create_event_authenticated_user(self):
        self.authenticate_user()
        response = self.client.post(reverse('event'), self.event_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)


class CreateUserViewTest(TestCase):

    def setUp(self):
        self.client = Client()
        self.user_data = {
            'username': 'testuser',
            'email': 'test@example.com',
            'password': 'testpassword'
        }
        self.create_user_url = reverse('create_user')

    def test_create_user(self):
        response = self.client.post(self.create_user_url, self.user_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)


class SerializerTest(TestCase):

    def test_event_serializer(self):
        organization = Organization.objects.create(
            title='Test Org',
            address='Test Address',
            postcode='12345'
        )
        event_data = {
            'title': 'Test Event',
            'description': 'Event Description',
            'organizations': [organization.id],
            'date': '2022-01-01T00:00:00Z',
        }
        serializer = EventSerializer(data=event_data)
        self.assertTrue(serializer.is_valid())

    def test_custom_user_serializer(self):
        user_data = {
            'username': 'testuser',
            'email': 'test@example.com',
            'password': 'testpassword'
        }
        serializer = CustomUserSerializer(data=user_data)
        self.assertTrue(serializer.is_valid())
