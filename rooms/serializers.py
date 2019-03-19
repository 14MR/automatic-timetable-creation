from rooms.models import Room, RoomType, Item, ItemType
from rest_framework import serializers


class ItemSerializer(serializers.ModelSerializer):
    type_id = serializers.PrimaryKeyRelatedField(source='type', queryset=ItemType.objects.all())
    room_id = serializers.PrimaryKeyRelatedField(source='room', queryset=Room.objects.all(), required=False)

    class Meta:
        model = Item
        fields = ('id', 'name', 'type_id', 'room_id')


class RoomTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = RoomType
        fields = ('id', 'name')


class ItemTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = RoomType
        fields = ('id', 'name')


class RoomSerializer(serializers.ModelSerializer):
    type_id = serializers.PrimaryKeyRelatedField(source='type', queryset=RoomType.objects.all())

    class Meta:
        model = Room
        fields = ('id', 'number', 'capacity', 'is_yellow', 'type_id',)
