from django.shortcuts import get_object_or_404
from rest_framework import viewsets, status, serializers
from rest_framework.decorators import action
from rest_framework.response import Response
from rooms.serializers import RoomSerializer, Room, Item, ItemSerializer, RoomType, RoomTypeSerializer
from rest_framework.permissions import AllowAny


class RoomViewSet(viewsets.ModelViewSet):
    serializer_class = RoomSerializer
    permission_classes = [AllowAny]

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
        self.perform_destroy(instance)
        return Response(data, status=status.HTTP_204_NO_CONTENT)

    @action(detail=False, methods=['get'])
    def types(self, request, pk=None):
        queryset = RoomType.objects.all()
        serializer = RoomTypeSerializer(data=queryset, many=True)
        serializer.is_valid()
        return Response(serializer.data, status=status.HTTP_200_OK)

    @action(detail=True, methods=['post'])
    def items(self, request, pk=None):
        queryset_rooms = Room.objects.all()
        queryset_items = Item.objects.all()
        room = get_object_or_404(queryset_rooms, pk=pk)
        item = get_object_or_404(queryset_items, pk=request.data['item_id'])
        room.items.add(item)  # TODO: check this
        return Response(ItemSerializer(item).data, status=status.HTTP_200_OK)


class ItemViewSet(viewsets.ModelViewSet):
    serializer_class = ItemSerializer
    permission_classes = [AllowAny]

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
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

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
        instance.delete()
        self.perform_destroy(instance)
        return Response(data, status=status.HTTP_204_NO_CONTENT)
