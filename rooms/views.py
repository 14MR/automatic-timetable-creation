from django.shortcuts import get_object_or_404
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response

from rooms.models import ItemType
from rooms.serializers import (
    RoomSerializer,
    Room,
    Item,
    ItemSerializer,
    RoomType,
    RoomTypeSerializer,
    ItemTypeSerializer,
)
from rest_framework import permissions


class RoomViewSet(viewsets.ModelViewSet):
    serializer_class = RoomSerializer
    permission_classes = () # permission level 0 or 1, building administrators

    def get_queryset(self):
        return Room.objects.all()

    def retrieve(self, request, pk=None):
        queryset = Room.objects.all()
        room = get_object_or_404(queryset, pk=pk)
        serializer = RoomSerializer(room)
        return Response(serializer.data)

    def create(self, request, *args, **kwargs):
        serializer = RoomSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def perform_create(self, serializer):
        serializer.save()

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        data = RoomSerializer(instance).data
        instance.delete()
        return Response(data, status=status.HTTP_204_NO_CONTENT)

    @action(detail=False, methods=["get"])
    def types(self, request, pk=None):
        queryset = RoomType.objects.all()
        serializer = RoomTypeSerializer(data=queryset, many=True)
        serializer.is_valid()
        return Response(serializer.data, status=status.HTTP_200_OK)

    @action(detail=True, methods=["post", "get"])
    def items(self, request, pk=None):
        if request.method == "POST":
            queryset_rooms = Room.objects.all()
            room = get_object_or_404(queryset_rooms, pk=pk)

            items = ItemSerializer(data=request.data, many=True)
            items.is_valid(raise_exception=True)
            for item in items.data:
                item["room"] = room
                Item.objects.create(**item)
            return Response(status=status.HTTP_201_CREATED)
        elif request.method == "GET":
            get_object_or_404(Room.objects.all(), pk=pk)
            queryset_items = Item.objects.filter(room=pk)
            return Response(
                ItemSerializer(queryset_items, many=True).data,
                status=status.HTTP_200_OK,
            )


class ItemViewSet(viewsets.ModelViewSet):
    serializer_class = ItemSerializer
    permission_classes = () # permission level 0 or 1, building administrators

    def get_queryset(self):
        return Item.objects.all()

    def retrieve(self, request, pk=None):
        queryset = self.get_queryset()
        item = get_object_or_404(queryset, pk=pk)
        serializer = ItemSerializer(item)
        return Response(serializer.data)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def perform_create(self, serializer):
        serializer.save()

    def update(self, request, pk=None):
        queryset = self.get_queryset()
        model = get_object_or_404(queryset, pk=pk)
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        instance = serializer.update(model, request.data)
        serializer = ItemSerializer(instance)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        data = ItemSerializer(instance).data
        self.perform_destroy(instance)
        return Response(data, status=status.HTTP_204_NO_CONTENT)

    @action(detail=False, methods=["get"])
    def types(self, request, pk=None):
        queryset = ItemType.objects.all()
        return Response(
            ItemTypeSerializer(queryset, many=True).data, status=status.HTTP_200_OK
        )
