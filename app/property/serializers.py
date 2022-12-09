"""
Serializers for recipe APIs
"""
from rest_framework import serializers

from core.models import Property


class PropertySerializer(serializers.ModelSerializer):
    """Serializer for properties."""

    class Meta:
        model = Property
        fields = ['id', 'name', 'city', 'price']
        read_only_fields = ['id']