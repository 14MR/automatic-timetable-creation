from rooms.models import Room, RoomType, Item, ItemType
from rest_framework import serializers


class ItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = Item
        fields = ('id', 'name')


class RoomTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = RoomType
        fields = ('id', 'name')


class RoomSerializer(serializers.ModelSerializer):
    items = ItemSerializer(required=False, many=True)
    type = RoomTypeSerializer()  # TODO : TYPE ID

    class Meta:
        model = Room
        fields = ('id', 'number', 'capacity', 'is_yellow', 'type', 'items')


class CreateRoomSerializer(serializers.ModelSerializer):
    class Meta:
        model = Room
        fields = ('id', 'number', 'capacity', 'is_yellow', 'type')
