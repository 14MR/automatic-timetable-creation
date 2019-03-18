from rooms.models import Room, RoomType, Item, ItemType
from rest_framework import serializers


class ItemSerializer(serializers.ModelSerializer):
    type_id = serializers.PrimaryKeyRelatedField(source='type', queryset=ItemType.objects.all())
    room_id = serializers.PrimaryKeyRelatedField(source='room', queryset=Room.objects.all())

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
    items = ItemSerializer(required=False, many=True)
    type_id = serializers.PrimaryKeyRelatedField(source='type', queryset=RoomType.objects.all())

    class Meta:
        model = Room
        fields = ('id', 'number', 'capacity', 'is_yellow', 'type_id', 'items')

    def create(self, validated_data):
        items_data = validated_data.pop('items')
        item_list = []
        for item in items_data:
            item_list.append(Item.objects.create(**item))
        room = Room.objects.create(**validated_data)
        room.items.set(item_list)
        return room
