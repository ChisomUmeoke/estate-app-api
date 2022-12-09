"""
Tests for properties APIs.
"""
from decimal import Decimal

from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from rest_framework import status
from rest_framework.test import APIClient

from core.models import Property

from property.serializers import(
     PropertySerializer,
     PropertyDetailSerializer
)


PROPERTIES_URL = reverse('property:property-list')

def detail_url(property_id):
    """Create and return a property detail URL."""
    return reverse('property:property-detail', args=[property_id])

def create_property(user, **params):
    """Create and return a sample propert."""
    defaults = {
        'name': 'executive apartment',
        'price': Decimal('100000'),
        'city': 'lagos',
    }
    defaults.update(params)

    property = Property.objects.create(user=user, **defaults)
    return property


class PublicPropertyAPITests(TestCase):
    """Test unauthenticated API requests."""

    def setUp(self):
        self.client = APIClient()

    def test_auth_required(self):
        """Test auth is required to call API."""
        res = self.client.get(PROPERTIES_URL)

        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class PrivatePropertyApiTests(TestCase):
    """Test authenticated API requests."""

    def setUp(self):
        self.client = APIClient()
        self.user = get_user_model().objects.create_user(
            'user@example.com',
            'testpass123',
        )
        self.client.force_authenticate(self.user)

    def test_retrieve_properties(self):
        """Test retrieving a list of properties."""
        create_property(user=self.user)
        create_property(user=self.user)

        res = self.client.get(PROPERTIES_URL)

        properties = Property.objects.all().order_by('-id')
        serializer = PropertySerializer(properties, many=True)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)

    def test_property_list_limited_to_user(self):
        """Test list of properties is limited to authenticated user."""
        other_user = get_user_model().objects.create_user(
            'other@example.com',
            'password123',
        )
        create_property(user=other_user)
        create_property(user=self.user)

        res = self.client.get(PROPERTIES_URL)

        properties = Property.objects.filter(user=self.user)
        serializer = PropertySerializer(properties, many=True)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)

    def test_get_property_detail(self):
        """Test get property detail."""
        property = create_property(user=self.user)

        url = detail_url(property.id)
        res = self.client.get(url)

        serializer = PropertyDetailSerializer(property)
        self.assertEqual(res.data, serializer.data)