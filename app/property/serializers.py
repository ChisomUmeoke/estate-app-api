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

class PropertyDetailSerializer(PropertySerializer):
    """Serializer for recipe detail view."""

    class Meta(PropertySerializer.Meta):
        fields = PropertySerializer.Meta.fields + ['name']