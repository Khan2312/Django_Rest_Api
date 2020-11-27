from rest_framework import viewsets
from myapi import serializers
from core.models import Content


class ContentViewSet(viewsets.ModelViewSet):
    """ Viewset for Content with all the methods """
    serializer_class = serializers.ContentSerializer
    queryset = Content.objects.all()
    filterset_fields = ['id']

    def perform_create(self, serializer):
        """Create a new object"""
        x = int(serializer.validated_data['x'])
        y = int(serializer.validated_data['y'])
        serializer.save(z=x*y)
