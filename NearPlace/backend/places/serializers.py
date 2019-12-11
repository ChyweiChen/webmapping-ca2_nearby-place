from rest_framework import serializers

from .models import Place


class PlaceSerializer(serializers.ModelSerializer):
    distance = serializers.CharField(source='get_distance')
    waypoint = serializers.JSONField(source='get_waypoint')

    class Meta:
        model = Place
        fields = '__all__'
