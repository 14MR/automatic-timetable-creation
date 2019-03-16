from rooms.models import Room, RoomType, Item, ItemType
from rest_framework import serializers


class ItemTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = ItemType
        fields = ('id', 'name')


class ItemSerializer(serializers.ModelSerializer):
    type = ItemTypeSerializer()

    class Meta:
        model = Item
        fields = ('id', 'name', 'type')


class RoomTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = RoomType
        fields = ('id', 'name')


class RoomSerializer(serializers.ModelSerializer):
    type = RoomTypeSerializer()

    class Meta:
        model = Room
        fields = ('id', 'number', 'capacity', 'is_yellow', 'type')
