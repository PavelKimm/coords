from rest_framework import serializers

from routes.models import Point


class PointListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Point
        fields = '__all__'
