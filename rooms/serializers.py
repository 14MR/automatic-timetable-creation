from rooms.models import Room
from rest_framework import serializers


class RoomSerializer(serializers.ModelSerializer):
    class Meta:
        model = Room
        fields = ('id', 'number', 'capacity', 'is_yellow')

