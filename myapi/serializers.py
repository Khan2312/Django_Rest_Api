from rest_framework import serializers
from core.models import Content


class ContentSerializer(serializers.ModelSerializer):
    """Serializer for Content object"""
    class Meta:
        model = Content
        fields = '__all__'
        read_only_Fields = ('id', 'x', 'y')
