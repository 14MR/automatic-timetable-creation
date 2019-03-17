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
    type_id = serializers.PrimaryKeyRelatedField(source='type', queryset=RoomType.objects.all())

    class Meta:
        model = Room
        fields = ('id', 'number', 'capacity', 'is_yellow', 'type_id', 'items')


class CreateRoomSerializer(serializers.ModelSerializer):
    class Meta:
        model = Room
        fields = ('id', 'number', 'capacity', 'is_yellow', 'type')
