"""
Views for the property APIs
"""
from rest_framework import viewsets
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated

from core.models import Property
from property import serializers


class PropertyViewSet(viewsets.ModelViewSet):
    """View for manage property APIs."""
    serializer_class = serializers.PropertySerializer
    queryset = Property.objects.all()
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        """Retrieve properties for authenticated user."""
        return self.queryset.filter(user=self.request.user).order_by('-id')